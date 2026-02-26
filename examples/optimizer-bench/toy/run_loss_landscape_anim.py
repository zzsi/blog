from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path

from loss_landscape_anim.main import loss_landscape_anim

SUPPORTED_OPTIMIZERS = ("adam", "sgd", "adagrad", "rmsprop")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate illustrative optimizer trajectory animations using loss-landscape-anim."
    )
    parser.add_argument(
        "--optimizers",
        nargs="+",
        default=list(SUPPORTED_OPTIMIZERS),
        help=f"Optimizers to run. Supported: {', '.join(SUPPORTED_OPTIMIZERS)}",
    )
    parser.add_argument("--epochs", type=int, default=120)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--frames", type=int, default=180)
    parser.add_argument("--gpus", type=int, default=0)
    parser.add_argument(
        "--outdir",
        type=str,
        default="outputs",
        help="Directory for GIFs and summary CSV.",
    )
    return parser.parse_args()


def run_one(optimizer: str, args: argparse.Namespace, outdir: Path) -> dict[str, float | str]:
    output_filename = str(outdir / f"spirals_{optimizer}.gif")
    optim_path, loss_steps, acc_steps = loss_landscape_anim(
        n_epochs=args.epochs,
        optimizer=optimizer,
        reduction_method="pca",
        output_to_file=True,
        output_filename=output_filename,
        giffps=args.fps,
        n_frames=args.frames,
        seed=args.seed,
        return_data=True,
        load_model=False,
        gpus=args.gpus,
    )

    final_loss = float(loss_steps[-1])
    final_acc = float(acc_steps[-1])
    return {
        "optimizer": optimizer,
        "n_steps_recorded": len(loss_steps),
        "final_loss": final_loss,
        "final_accuracy": final_acc,
        "final_perplexity_like": math.exp(min(20.0, final_loss)),
        "gif_path": output_filename,
    }


def main() -> None:
    args = parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    bad = [opt for opt in args.optimizers if opt not in SUPPORTED_OPTIMIZERS]
    if bad:
        raise ValueError(
            f"Unsupported optimizers: {bad}. Supported: {SUPPORTED_OPTIMIZERS}. "
            "loss-landscape-anim natively supports adam/sgd/adagrad/rmsprop."
        )

    rows: list[dict[str, float | str]] = []
    for opt in args.optimizers:
        print(f"=== Running toy landscape animation for optimizer={opt} ===")
        row = run_one(opt, args, outdir)
        rows.append(row)
        print(
            f"done optimizer={opt} final_loss={row['final_loss']:.4f} "
            f"final_accuracy={row['final_accuracy']:.4f} gif={row['gif_path']}"
        )

    summary_path = outdir / "summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "optimizer",
                "n_steps_recorded",
                "final_loss",
                "final_accuracy",
                "final_perplexity_like",
                "gif_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote summary: {summary_path}")


if __name__ == "__main__":
    main()
