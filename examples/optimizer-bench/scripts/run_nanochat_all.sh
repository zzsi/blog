#!/usr/bin/env bash
set -euo pipefail

optimizers=(sgd_momentum adamw lamb adafactor sam muon)
for opt in "${optimizers[@]}"; do
  echo "=== NANOCHAT | optimizer=${opt} ==="
  python train.py task=nanochat optimizer=${opt} run.max_steps=150 run.eval_every=50 run.log_every=25 run.batch_size=16
  echo
  sleep 1
done
