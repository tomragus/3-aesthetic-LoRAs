"""FAL-based inference for comparing adapter output against the base Krea 2 model."""

import fal_client

KREA_2_MODEL = "REPLACE_WITH_FAL_KREA_2_MODEL_ID"


def generate_image(prompt: str, adapter_path: str | None = None):
    """Generate a test image via FAL, optionally applying a trained LoRA adapter."""
    arguments = {"prompt": prompt}
    if adapter_path:
        arguments["loras"] = [{"path": adapter_path}]

    result = fal_client.run(KREA_2_MODEL, arguments=arguments)
    return result
