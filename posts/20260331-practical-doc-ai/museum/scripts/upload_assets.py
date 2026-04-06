#!/usr/bin/env python3
"""Upload generated Room 1 assets to Hugging Face dataset repo.

Usage:
    python scripts/upload_assets.py                  # upload room1 assets
    python scripts/upload_assets.py --dry-run        # list files without uploading

Requires:
    pip install huggingface_hub
    huggingface-cli login  (or set HF_TOKEN env var)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import HfApi

REPO_ID = "zzsi/blog_assets"
REPO_TYPE = "dataset"

# Mapping of local asset dirs to HF paths
UPLOAD_CONFIGS = {
    "room1": {
        "local_dir": Path(__file__).resolve().parents[1] / "assets" / "room1" / "generated",
        "hf_prefix": "docai/template-registration-ocr-employment-forms",
    },
}


def collect_files(local_dir: Path) -> list[Path]:
    """Collect all files to upload, excluding hidden files and __pycache__."""
    files = []
    for path in sorted(local_dir.rglob("*")):
        if path.is_file() and not any(part.startswith(".") or part == "__pycache__" for part in path.parts):
            files.append(path)
    return files


def upload_room(room: str, dry_run: bool = False) -> None:
    config = UPLOAD_CONFIGS[room]
    local_dir = config["local_dir"]
    hf_prefix = config["hf_prefix"]

    if not local_dir.exists():
        print(f"Directory not found: {local_dir}")
        return

    files = collect_files(local_dir)
    if not files:
        print(f"No files found in {local_dir}")
        return

    print(f"{'[DRY RUN] ' if dry_run else ''}Uploading {len(files)} files from {local_dir}")
    print(f"  -> {REPO_ID} / {hf_prefix}/")

    if dry_run:
        for f in files:
            rel = f.relative_to(local_dir)
            print(f"  {rel}  ->  {hf_prefix}/{rel}")
        return

    api = HfApi()
    api.upload_folder(
        folder_path=str(local_dir),
        path_in_repo=hf_prefix,
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
    )
    print(f"Done. Files available at:")
    print(f"  https://huggingface.co/datasets/{REPO_ID}/tree/main/{hf_prefix}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload museum assets to Hugging Face")
    parser.add_argument("--room", default="room1", choices=list(UPLOAD_CONFIGS.keys()),
                        help="Which room's assets to upload (default: room1)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List files without uploading")
    args = parser.parse_args()

    upload_room(args.room, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
