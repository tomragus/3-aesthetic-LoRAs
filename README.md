# 3 Aesthetic LoRAs

Three LoRA adapters trained on the Krea 2 base model, each capturing a distinct aesthetic via a trigger phrase:

- **Ghibli-style**
- **Broad-stroke minimal color**
- **Hand-drawn / gritty**

Each adapter is trained on its own ~1000-image Hugging Face dataset with existing captions, using one shared training script driven by per-adapter configs.

## Structure

- `src/` — shared training, data-loading, logging, and inference code
- `configs/` — one YAML config per adapter (`ghibli.yaml`, `broadstroke.yaml`, `handsketch.yaml`)
- `scripts/` — one-off utilities (dataset download, caption editing, Trackio launch)
- `data/` — downloaded datasets (git-ignored, populated locally via `scripts/download_data.py`)

## Usage

```
python src/train.py --config configs/ghibli.yaml
```

## Compute & tracking

- Training runs on a RunPod A40 GPU pod, developed locally and executed remotely via SSH.
- Training progress is tracked with Trackio, connected to a Hugging Face Space.
- Test generations (before/during/after training) use FAL, a third-party inference API, kept separate from RunPod training compute.

## Model weights

This repo holds code and config only. Each adapter's trained weights, adapter config, and model card live in their own Hugging Face model repo, pushed manually once that adapter's training run finishes.
