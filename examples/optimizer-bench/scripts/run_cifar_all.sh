#!/usr/bin/env bash
set -euo pipefail

optimizers=(sgd_momentum adamw lamb adafactor sam muon)
for opt in "${optimizers[@]}"; do
  echo "=== CIFAR10 | optimizer=${opt} ==="
  python train.py task=cifar10 optimizer=${opt} run.max_steps=200 run.eval_every=50 run.log_every=20
  echo
  sleep 1
done
