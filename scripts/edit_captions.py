"""Review and edit captions for a downloaded dataset without touching the original hosted data.

Reads captions from data/<aesthetic>/captions/ and writes edits to
data/<aesthetic>/captions_edited/, keeping raw and edited captions in
separate files so re-running download_data.py never clobbers edits.

Usage:
    python scripts/edit_captions.py --aesthetic ghibli
"""

import argparse
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--aesthetic", required=True, choices=["ghibli", "broadstroke", "handsketch"])
    return parser.parse_args()


def init_edited_captions(aesthetic: str, data_dir: str = "data"):
    """Copy raw captions into the edited-captions folder if it doesn't exist yet."""
    raw_dir = Path(data_dir) / aesthetic / "captions"
    edited_dir = Path(data_dir) / aesthetic / "captions_edited"

    if edited_dir.exists():
        return edited_dir

    edited_dir.mkdir(parents=True)
    for caption_file in raw_dir.glob("*.txt"):
        shutil.copy(caption_file, edited_dir / caption_file.name)
    return edited_dir


if __name__ == "__main__":
    args = parse_args()
    edited_dir = init_edited_captions(args.aesthetic)
    print(f"Edit captions in: {edited_dir}")
