"""Shared LoRA training entrypoint, driven by a per-adapter config.

Usage:
    python src/train.py --config configs/ghibli.yaml
"""

import argparse

import yaml

from data_utils import build_dataloader, load_dataset
from logging_utils import init_logging, log_metrics


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to the adapter's YAML config")
    return parser.parse_args()


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    args = parse_args()
    config = load_config(args.config)

    init_logging(run_name=config["trigger_phrase"], config=config)

    dataset = load_dataset(config["dataset_path"], config["trigger_phrase"])
    dataloader = build_dataloader(dataset, config["hyperparameters"]["batch_size"])

    raise NotImplementedError("training loop not yet implemented")


if __name__ == "__main__":
    main()
