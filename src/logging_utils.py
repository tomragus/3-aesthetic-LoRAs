"""Shared Trackio logging for LoRA training runs."""


def init_logging(run_name: str, config: dict):
    """Start a Trackio run for this training config."""
    raise NotImplementedError


def log_metrics(step: int, metrics: dict):
    """Log training metrics for the current step."""
    raise NotImplementedError
