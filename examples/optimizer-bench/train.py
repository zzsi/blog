from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any, Iterator

import hydra
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from datasets import load_dataset
from omegaconf import DictConfig
from torch.utils.data import DataLoader, Dataset, Subset
from torchvision import datasets as tv_datasets
from torchvision import transforms
from transformers import Adafactor, AutoTokenizer

from optimizers import LAMB, MuonLite, SAM


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def resolve_device(device_cfg: str) -> torch.device:
    if device_cfg != "auto":
        return torch.device(device_cfg)
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


class SmallCnn(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(128 * 8 * 8, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class TinyCausalLm(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        model_dim: int,
        num_layers: int,
        num_heads: int,
        ffn_dim: int,
        max_len: int,
        dropout: float,
    ):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, model_dim)
        self.pos_emb = nn.Embedding(max_len, model_dim)
        layer = nn.TransformerEncoderLayer(
            d_model=model_dim,
            nhead=num_heads,
            dim_feedforward=ffn_dim,
            dropout=dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=num_layers)
        self.norm = nn.LayerNorm(model_dim)
        self.lm_head = nn.Linear(model_dim, vocab_size)
        self.max_len = max_len

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        bsz, seqlen = input_ids.shape
        if seqlen > self.max_len:
            raise ValueError(f"sequence length {seqlen} > max_len {self.max_len}")
        positions = torch.arange(seqlen, device=input_ids.device).unsqueeze(0).expand(bsz, -1)
        x = self.token_emb(input_ids) + self.pos_emb(positions)
        mask = torch.triu(torch.ones(seqlen, seqlen, device=input_ids.device), diagonal=1).bool()
        x = self.encoder(x, mask=mask)
        x = self.norm(x)
        return self.lm_head(x)


class LmDataset(Dataset):
    def __init__(self, token_chunks: list[list[int]]):
        self.token_chunks = token_chunks

    def __len__(self) -> int:
        return len(self.token_chunks)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        ids = torch.tensor(self.token_chunks[idx], dtype=torch.long)
        return {
            "input_ids": ids[:-1],
            "labels": ids[1:],
        }


def _text_from_record(record: dict[str, Any], text_field: str) -> str:
    if text_field != "auto" and text_field in record and isinstance(record[text_field], str):
        return record[text_field]

    candidate_keys = ["text", "content", "prompt", "response", "instruction"]
    for key in candidate_keys:
        val = record.get(key)
        if isinstance(val, str) and val.strip():
            return val

    for val in record.values():
        if isinstance(val, str) and val.strip():
            return val
        if isinstance(val, list):
            parts = [v for v in val if isinstance(v, str) and v.strip()]
            if parts:
                return "\n".join(parts)

    return ""


def _batch_iter(loader: DataLoader) -> Iterator[Any]:
    while True:
        for batch in loader:
            yield batch


def load_cifar(cfg: DictConfig) -> tuple[nn.Module, DataLoader, DataLoader]:
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
        ]
    )
    train_ds = tv_datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)
    test_ds = tv_datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)

    train_subset = Subset(train_ds, list(range(min(cfg.task.train_subset, len(train_ds)))))
    val_subset = Subset(test_ds, list(range(min(cfg.task.val_subset, len(test_ds)))))

    train_loader = DataLoader(
        train_subset,
        batch_size=cfg.run.batch_size,
        shuffle=True,
        num_workers=cfg.run.num_workers,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_subset,
        batch_size=cfg.run.batch_size,
        shuffle=False,
        num_workers=cfg.run.num_workers,
        pin_memory=True,
    )
    model = SmallCnn(num_classes=cfg.task.num_classes)
    return model, train_loader, val_loader


def load_nanochat(cfg: DictConfig) -> tuple[nn.Module, DataLoader, DataLoader]:
    ds_train = load_dataset(cfg.task.hf_dataset, split=cfg.task.train_split)
    ds_val = load_dataset(cfg.task.hf_dataset, split=cfg.task.val_split)

    if cfg.task.train_subset > 0:
        ds_train = ds_train.select(range(min(len(ds_train), cfg.task.train_subset)))
    if cfg.task.val_subset > 0:
        ds_val = ds_val.select(range(min(len(ds_val), cfg.task.val_subset)))

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    if tokenizer.eos_token_id is None:
        raise RuntimeError("Tokenizer must provide eos_token_id")

    block = int(cfg.task.block_size)

    def build_chunks(ds) -> list[list[int]]:
        chunks: list[list[int]] = []
        for record in ds:
            text = _text_from_record(record, cfg.task.text_field)
            if not text:
                continue
            ids = tokenizer.encode(text, add_special_tokens=False)
            if len(ids) < 2:
                continue
            ids = ids[: block * 8] + [tokenizer.eos_token_id]
            start = 0
            while start + block + 1 <= len(ids):
                chunks.append(ids[start : start + block + 1])
                start += block
        return chunks

    train_chunks = build_chunks(ds_train)
    val_chunks = build_chunks(ds_val)

    if not train_chunks or not val_chunks:
        raise RuntimeError(
            "No usable text chunks were built from nanochat. Adjust text_field or subset settings."
        )

    train_loader = DataLoader(
        LmDataset(train_chunks),
        batch_size=cfg.run.batch_size,
        shuffle=True,
        num_workers=cfg.run.num_workers,
        pin_memory=True,
    )
    val_loader = DataLoader(
        LmDataset(val_chunks),
        batch_size=cfg.run.batch_size,
        shuffle=False,
        num_workers=cfg.run.num_workers,
        pin_memory=True,
    )

    model = TinyCausalLm(
        vocab_size=cfg.task.vocab_size,
        model_dim=cfg.task.model_dim,
        num_layers=cfg.task.num_layers,
        num_heads=cfg.task.num_heads,
        ffn_dim=cfg.task.ffn_dim,
        max_len=block,
        dropout=cfg.task.dropout,
    )
    return model, train_loader, val_loader


def build_optimizer(cfg: DictConfig, model: nn.Module):
    params = model.parameters()
    name = cfg.optimizer.name

    if name == "sgd_momentum":
        return torch.optim.SGD(
            params,
            lr=cfg.optimizer.lr,
            momentum=cfg.optimizer.momentum,
            nesterov=cfg.optimizer.nesterov,
            weight_decay=cfg.optimizer.weight_decay,
        )

    if name == "adamw":
        return torch.optim.AdamW(
            params,
            lr=cfg.optimizer.lr,
            betas=tuple(cfg.optimizer.betas),
            weight_decay=cfg.optimizer.weight_decay,
        )

    if name == "lamb":
        return LAMB(
            params,
            lr=cfg.optimizer.lr,
            betas=tuple(cfg.optimizer.betas),
            eps=cfg.optimizer.eps,
            weight_decay=cfg.optimizer.weight_decay,
        )

    if name == "adafactor":
        return Adafactor(
            params,
            lr=cfg.optimizer.lr,
            weight_decay=cfg.optimizer.weight_decay,
            relative_step=cfg.optimizer.relative_step,
            scale_parameter=cfg.optimizer.scale_parameter,
            warmup_init=cfg.optimizer.warmup_init,
        )

    if name == "sam":
        base = torch.optim.SGD(
            params,
            lr=cfg.optimizer.lr,
            momentum=cfg.optimizer.momentum,
            nesterov=cfg.optimizer.nesterov,
            weight_decay=cfg.optimizer.weight_decay,
        )
        return SAM(model.parameters(), base_optimizer=base, rho=cfg.optimizer.rho)

    if name == "muon":
        return MuonLite(
            params,
            lr=cfg.optimizer.lr,
            momentum=cfg.optimizer.momentum,
            weight_decay=cfg.optimizer.weight_decay,
            eps=cfg.optimizer.eps,
        )

    raise ValueError(f"Unknown optimizer: {name}")


@torch.no_grad()
def eval_cifar(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    total = 0
    correct = 0
    for x, y in loader:
        x = x.to(device, non_blocking=True)
        y = y.to(device, non_blocking=True)
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        total_loss += loss.item() * y.size(0)
        pred = logits.argmax(dim=1)
        correct += (pred == y).sum().item()
        total += y.size(0)
    return total_loss / max(total, 1), correct / max(total, 1)


@torch.no_grad()
def eval_lm(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    total_tokens = 0
    for batch in loader:
        input_ids = batch["input_ids"].to(device, non_blocking=True)
        labels = batch["labels"].to(device, non_blocking=True)
        logits = model(input_ids)
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), labels.reshape(-1), reduction="sum")
        total_loss += loss.item()
        total_tokens += labels.numel()
    nll = total_loss / max(total_tokens, 1)
    ppl = math.exp(min(20.0, nll))
    return nll, ppl


def train_cifar(cfg: DictConfig, model: nn.Module, train_loader: DataLoader, val_loader: DataLoader, optimizer, device: torch.device):
    model.train()
    step_iter = _batch_iter(train_loader)

    for step in range(1, cfg.run.max_steps + 1):
        x, y = next(step_iter)
        x = x.to(device, non_blocking=True)
        y = y.to(device, non_blocking=True)

        if cfg.optimizer.name == "sam":
            optimizer.zero_grad()
            loss = F.cross_entropy(model(x), y)
            loss.backward()
            optimizer.first_step()

            optimizer.zero_grad()
            loss2 = F.cross_entropy(model(x), y)
            loss2.backward()
            optimizer.second_step()
            loss_value = loss2.item()
        else:
            optimizer.zero_grad()
            logits = model(x)
            loss = F.cross_entropy(logits, y)
            loss.backward()
            optimizer.step()
            loss_value = loss.item()

        if step % cfg.run.log_every == 0:
            print(f"step={step} train_loss={loss_value:.4f}")

        if step % cfg.run.eval_every == 0:
            val_loss, val_acc = eval_cifar(model, val_loader, device)
            print(f"step={step} val_loss={val_loss:.4f} val_acc={val_acc:.4f}")
            model.train()


def train_lm(cfg: DictConfig, model: nn.Module, train_loader: DataLoader, val_loader: DataLoader, optimizer, device: torch.device):
    model.train()
    step_iter = _batch_iter(train_loader)

    for step in range(1, cfg.run.max_steps + 1):
        batch = next(step_iter)
        input_ids = batch["input_ids"].to(device, non_blocking=True)
        labels = batch["labels"].to(device, non_blocking=True)

        if cfg.optimizer.name == "sam":
            optimizer.zero_grad()
            logits = model(input_ids)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), labels.reshape(-1))
            loss.backward()
            optimizer.first_step()

            optimizer.zero_grad()
            logits2 = model(input_ids)
            loss2 = F.cross_entropy(logits2.view(-1, logits2.size(-1)), labels.reshape(-1))
            loss2.backward()
            optimizer.second_step()
            loss_value = loss2.item()
        else:
            optimizer.zero_grad()
            logits = model(input_ids)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), labels.reshape(-1))
            loss.backward()
            optimizer.step()
            loss_value = loss.item()

        if step % cfg.run.log_every == 0:
            print(f"step={step} train_nll={loss_value:.4f} train_ppl={math.exp(min(20.0, loss_value)):.2f}")

        if step % cfg.run.eval_every == 0:
            val_nll, val_ppl = eval_lm(model, val_loader, device)
            print(f"step={step} val_nll={val_nll:.4f} val_ppl={val_ppl:.2f}")
            model.train()


@hydra.main(config_path="configs", config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:
    set_seed(cfg.seed)
    device = resolve_device(cfg.device)
    print(f"task={cfg.task.name} optimizer={cfg.optimizer.name} device={device}")

    if cfg.task.name == "cifar10":
        model, train_loader, val_loader = load_cifar(cfg)
    elif cfg.task.name == "nanochat":
        model, train_loader, val_loader = load_nanochat(cfg)
    else:
        raise ValueError(f"Unknown task: {cfg.task.name}")

    model.to(device)
    optimizer = build_optimizer(cfg, model)

    if cfg.task.name == "cifar10":
        train_cifar(cfg, model, train_loader, val_loader, optimizer, device)
        val_loss, val_acc = eval_cifar(model, val_loader, device)
        print(f"final val_loss={val_loss:.4f} val_acc={val_acc:.4f}")
    else:
        train_lm(cfg, model, train_loader, val_loader, optimizer, device)
        val_nll, val_ppl = eval_lm(model, val_loader, device)
        print(f"final val_nll={val_nll:.4f} val_ppl={val_ppl:.2f}")


if __name__ == "__main__":
    main()
