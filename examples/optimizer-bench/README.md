# Optimizer Bench (CIFAR-10 + NanoGPT-Style LM)

Minimal Hydra-based benchmark project to compare six optimizers under one codepath:

- `sgd_momentum`
- `adamw`
- `lamb`
- `adafactor`
- `sam`
- `muon` (`MuonLite` proxy for directional conditioning)

## Tasks in scope now

- `cifar10` classification
- `nanogpt_bin` language modeling from local `train.bin`/`val.bin`

## TODO

- Add image-generation benchmark on `CelebA-HQ` or `FFHQ`.

## Setup

```bash
cd examples/optimizer-bench
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Prepare local LM data (NanoGPT style)

This benchmark expects local bin artifacts, not a Hugging Face dataset ID.

```bash
git clone https://github.com/karpathy/nanoGPT /tmp/cvl/nanogpt
cd /tmp/cvl/nanogpt
python3 data/shakespeare/prepare.py
# Creates:
#   /tmp/cvl/nanogpt/data/shakespeare/train.bin
#   /tmp/cvl/nanogpt/data/shakespeare/val.bin
```

## Run one experiment

```bash
python train.py task=cifar10 optimizer=adamw
python train.py task=nanochat task.data_dir=/tmp/cvl/nanogpt/data/shakespeare optimizer=lamb run.max_steps=100 run.batch_size=16
```

## Run all six optimizers

```bash
./scripts/run_cifar_all.sh
export NANOGPT_DATA_DIR=/tmp/cvl/nanogpt/data/shakespeare
./scripts/run_nanochat_all.sh
```

## Notes

- `sam` uses a two-step update, so wall-clock is expected to be slower.
- `muon` in this project is a lightweight proxy (`MuonLite`) for small-demo behavior comparisons, not a claim of exact algorithm parity with full Muon implementations.
- Keep tuning budgets matched across optimizers for fair comparison.
