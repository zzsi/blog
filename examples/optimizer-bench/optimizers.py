from __future__ import annotations

from typing import Iterable

import torch
from torch.optim import Optimizer


class LAMB(Optimizer):
    """Minimal LAMB implementation for benchmarking demos."""

    def __init__(
        self,
        params: Iterable[torch.nn.Parameter],
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 0.0,
    ):
        defaults = dict(lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            beta1, beta2 = group["betas"]
            eps = group["eps"]
            lr = group["lr"]
            wd = group["weight_decay"]

            for p in group["params"]:
                if p.grad is None:
                    continue

                grad = p.grad
                if grad.is_sparse:
                    raise RuntimeError("LAMB does not support sparse gradients")

                state = self.state[p]
                if len(state) == 0:
                    state["step"] = 0
                    state["exp_avg"] = torch.zeros_like(p)
                    state["exp_avg_sq"] = torch.zeros_like(p)

                exp_avg = state["exp_avg"]
                exp_avg_sq = state["exp_avg_sq"]
                state["step"] += 1

                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

                denom = exp_avg_sq.sqrt().add_(eps)
                update = exp_avg / denom
                if wd > 0:
                    update = update.add(p, alpha=wd)

                w_norm = torch.norm(p).clamp(min=eps)
                u_norm = torch.norm(update).clamp(min=eps)
                trust_ratio = (w_norm / u_norm).clamp(max=10.0)

                p.add_(update, alpha=-lr * trust_ratio)

        return loss


class SAM:
    """Sharpness-Aware Minimization wrapper around a base optimizer."""

    def __init__(self, params: Iterable[torch.nn.Parameter], base_optimizer: Optimizer, rho: float = 0.05, eps: float = 1e-12):
        self.params = list(params)
        self.base_optimizer = base_optimizer
        self.rho = rho
        self.eps = eps

    def zero_grad(self):
        self.base_optimizer.zero_grad()

    @torch.no_grad()
    def _grad_norm(self) -> torch.Tensor:
        norms = []
        for p in self.params:
            if p.grad is not None:
                norms.append(torch.norm(p.grad, p=2))
        if not norms:
            return torch.tensor(0.0)
        return torch.norm(torch.stack(norms), p=2)

    @torch.no_grad()
    def first_step(self):
        grad_norm = self._grad_norm()
        scale = self.rho / (grad_norm + self.eps)
        for p in self.params:
            if p.grad is None:
                continue
            e_w = p.grad * scale
            p.add_(e_w)
            self.base_optimizer.state[p]["_sam_e_w"] = e_w

    @torch.no_grad()
    def second_step(self):
        for p in self.params:
            if p.grad is None:
                continue
            e_w = self.base_optimizer.state[p].pop("_sam_e_w", None)
            if e_w is not None:
                p.sub_(e_w)
        self.base_optimizer.step()


class MuonLite(Optimizer):
    """Lightweight proxy for Muon-style directional conditioning.

    This normalizes per-parameter gradients and applies momentum. It is not a
    drop-in replacement for the original Muon algorithm, but it is useful for
    demonstrating conditioning-like behavior in small demos.
    """

    def __init__(
        self,
        params: Iterable[torch.nn.Parameter],
        lr: float = 1e-2,
        momentum: float = 0.95,
        weight_decay: float = 0.0,
        eps: float = 1e-8,
    ):
        defaults = dict(lr=lr, momentum=momentum, weight_decay=weight_decay, eps=eps)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            lr = group["lr"]
            momentum = group["momentum"]
            wd = group["weight_decay"]
            eps = group["eps"]

            for p in group["params"]:
                if p.grad is None:
                    continue

                grad = p.grad
                if wd > 0:
                    grad = grad.add(p, alpha=wd)

                grad = grad / (grad.norm().clamp(min=eps))

                state = self.state[p]
                if len(state) == 0:
                    state["momentum_buffer"] = torch.zeros_like(p)

                buf = state["momentum_buffer"]
                buf.mul_(momentum).add_(grad, alpha=1 - momentum)
                p.add_(buf, alpha=-lr)

        return loss
