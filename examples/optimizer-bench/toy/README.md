# Toy Optimizer Visuals (loss-landscape-anim)

This module adds a didactic visual benchmark using
[`loss-landscape-anim`](https://github.com/logancyang/loss-landscape-anim).

It creates GIFs that show optimizer trajectories in a 2D PCA slice of the loss
landscape on a small spirals classification task.

## Why this exists

- It is highly illustrative for blog readers.
- It explains optimizer behavior (zig-zagging, curvature response, basin entry)
  before moving to heavier CIFAR-10/NanoGPT benchmarks.
- It is a toy benchmark and should not be treated as frontier-scale evidence.

## Supported optimizers

`loss-landscape-anim` natively supports:

- `adam`
- `sgd`
- `adagrad`
- `rmsprop`

## Setup

From `examples/optimizer-bench`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r toy/requirements.txt
```

### Compatibility note

`loss-landscape-anim` has strict transitive version constraints and can fail with
newest Torch/TorchVision combos. The pinned versions in `toy/requirements.txt`
are chosen to provide a reproducible run path for this repo.

## Run

```bash
cd toy
./run_toy_all.sh
```

Or run specific optimizers:

```bash
python run_loss_landscape_anim.py --optimizers adam sgd --epochs 100 --outdir outputs
```

For shared machines, force CPU-only mode to avoid unintended GPU/distributed usage:

```bash
CUDA_VISIBLE_DEVICES=\"\" python run_loss_landscape_anim.py --optimizers adam sgd --epochs 40 --gpus 0 --outdir outputs
```

## Outputs

- `outputs/spirals_<optimizer>.gif`
- `outputs/summary.csv`
