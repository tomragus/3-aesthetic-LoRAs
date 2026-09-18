"""Download the three aesthetic datasets from Hugging Face into the git-ignored data/ folder.

Usage:
    python scripts/download_data.py
"""

from huggingface_hub import snapshot_download

DATASETS = {
    "ghibli": "REPLACE_WITH_HF_DATASET_ID",
    "broadstroke": "REPLACE_WITH_HF_DATASET_ID",
    "handsketch": "REPLACE_WITH_HF_DATASET_ID",
}


def download_all(data_dir: str = "data"):
    for name, dataset_id in DATASETS.items():
        snapshot_download(
            repo_id=dataset_id,
            repo_type="dataset",
            local_dir=f"{data_dir}/{name}",
        )


if __name__ == "__main__":
    download_all()
