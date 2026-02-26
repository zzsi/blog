#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${NANOGPT_DATA_DIR:-}" ]]; then
  echo "Set NANOGPT_DATA_DIR to a directory with train.bin/val.bin first."
  echo "Example: export NANOGPT_DATA_DIR=/tmp/cvl/nanogpt/data/shakespeare"
  exit 1
fi

optimizers=(sgd_momentum adamw lamb adafactor sam muon)
for opt in "${optimizers[@]}"; do
  echo "=== NANOGPT_BIN | optimizer=${opt} ==="
  python train.py task=nanochat task.data_dir="${NANOGPT_DATA_DIR}" optimizer=${opt} run.max_steps=150 run.eval_every=50 run.log_every=25 run.batch_size=16
  echo
  sleep 1
done
