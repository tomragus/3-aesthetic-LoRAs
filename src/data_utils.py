"""Shared dataset loading for LoRA training runs."""


def load_dataset(dataset_path: str, trigger_phrase: str):
    """Load the captioned image dataset and prepend the trigger phrase to each caption."""
    raise NotImplementedError


def build_dataloader(dataset, batch_size: int):
    """Wrap the dataset in a dataloader for training."""
    raise NotImplementedError
