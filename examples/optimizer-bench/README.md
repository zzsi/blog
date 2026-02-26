# Optimizer Bench (CIFAR-10 + nanochat)

Minimal Hydra-based benchmark project to compare six optimizers under one codepath:

- `sgd_momentum`
- `adamw`
- `lamb`
- `adafactor`
- `sam`
- `muon` (`MuonLite` proxy for directional conditioning)

## Tasks in scope now

- `cifar10` classification
- `nanochat/nanochat` language modeling

## TODO

- Add image-generation benchmark on `CelebA-HQ` or `FFHQ`.

## Setup

```bash
cd examples/optimizer-bench
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run one experiment

```bash
python train.py task=cifar10 optimizer=adamw
python train.py task=nanochat optimizer=lamb run.max_steps=100 run.batch_size=16
```

## Run all six optimizers

```bash
./scripts/run_cifar_all.sh
./scripts/run_nanochat_all.sh
```

## Notes

- `sam` uses a two-step update, so wall-clock is expected to be slower.
- `muon` in this project is a lightweight proxy (`MuonLite`) for small-demo behavior comparisons, not a claim of exact algorithm parity with full Muon implementations.
- Keep tuning budgets matched across optimizers for fair comparison.
