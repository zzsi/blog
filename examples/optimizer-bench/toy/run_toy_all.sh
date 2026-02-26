#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python run_loss_landscape_anim.py \
  --optimizers adam sgd adagrad rmsprop \
  --epochs 120 \
  --fps 15 \
  --frames 180 \
  --seed 42 \
  --outdir outputs
