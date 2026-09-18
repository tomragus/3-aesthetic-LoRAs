# Krea 2 LoRA Adapters — Initial Repo Structure

## Objective

Set up the initial structure of the GitHub code repo for training three LoRA adapters on Krea 2, with shared training code and one config per adapter, ready for local development in Cursor with remote execution on a RunPod pod.

## Context

- Project: 3 LoRA adapters on the Krea 2 base model, each capturing a specific aesthetic via a trigger phrase — Ghibli-style, wide-stroke minimal color, and hand-drawn/gritty. Each aesthetic is backed by a ~1000-image Hugging Face dataset with existing captions.
- Compute: RunPod A40 GPU pod. Development happens locally in Cursor; code runs remotely on the pod via SSH.
- Tracking: Trackio, connected to a Hugging Face Space, for monitoring training runs.
- Inference for testing generations (before/during/after training): FAL, a third-party inference API, kept separate from RunPod training compute.
- Version control split: GitHub holds all code and config, with frequent commits as code is written. Hugging Face Hub holds three separate model repos (one per adapter), each receiving a manual push only when that adapter's training run is finished — not pushed in lockstep with GitHub commits. A single Hugging Face write-scope token works across all repos under the account.
- Training code is expected to be identical in logic across all three adapters — only data path, trigger phrase, and some hyperparameters differ — so one shared training script driven by per-adapter configs is the right shape, not three separate codebases.



## Decisions

- [Tom's answer] Downloaded datasets live in a git-ignored `data/` folder, not committed to GitHub.
- [Tom's answer] One shared training script, shared data-loading/logging code, and a `configs/` folder with three files (one per aesthetic) specifying dataset path, trigger phrase, and differing hyperparameters.
- [Tom's answer] FAL used for third-party inference, referenced directly in the code.
- [Tom's answer] GitHub repo = code and config only. Each adapter's Hugging Face model repo holds only trained weights, adapter config, and model card.
- [Tom's answer] Repo name is `3-aesthetic-LoRAs` on GitHub. The local clone's folder and `origin` remote currently say `finetuned-model-tbd` (mismatch to fix — see Step 1 below).
- [Tom's answer] Config file names: `ghibli.yaml`, `broadstroke.yaml`, `handsketch.yaml`.
- [Tom's answer] Steps 7 and 8 (RunPod environment file, Trackio/Space launch script) are included as committed boilerplate in this pass.
- [Tom's answer] `prompts-LoRA-adaptations.md` and `prompts-raw-turbo.md` (existing untracked scratch files with test-generation prompts) are left alone and added to `.gitignore` by name, not folded into the repo structure.
- [Tom's answer] `CLAUDE.md` is also added to `.gitignore` — not committed to GitHub.
- [Tom's answer] Implementation of this plan happens directly in the main thread, no subagent delegation.



## Steps

1. Fix repo/folder naming mismatch
  - Files: none (filesystem + git config only)
  - Execution: Rename the local folder from `finetuned-model-tbd` to `3-aesthetic-LoRAs`, and update the `origin` remote URL to point at `git@github.com:tomragus/3-aesthetic-LoRAs.git` (confirm the actual GitHub URL before changing it — it may differ from this guess).
  - Done when: Local folder name, git remote, and GitHub repo name all agree.
2. Initialize repo scaffolding and `.gitignore`
  - Files: `README.md`, `.gitignore`
  - Execution: Create the project folder, run `git init`, add a `.gitignore` excluding `data/`, checkpoints/output directories, `.env`, `__pycache__`, `CLAUDE.md`, `prompts-LoRA-adaptations.md`, `prompts-raw-turbo.md`, and other standard Python exclusions.
  - Done when: Repo has base scaffolding and a clean `git status`.
3. Set up the top-level directory structure
  - Files: `src/`, `configs/`, `data/` (empty, git-ignored), `scripts/`
  - Execution: Create `src/` for shared training, data-loading, and logging code; `configs/` for the three per-adapter YAML files; `data/` for downloaded datasets (git-ignored); `scripts/` for one-off utilities (dataset download, caption editing).
  - Done when: Directory tree matches this layout and is committed, except `data/` contents.
4. Add the shared training script and supporting modules
  - Files: `src/train.py`, `src/data_utils.py`, `src/logging_utils.py`
  - Execution: Write `train.py` to accept a config path as an argument (e.g. `python src/train.py --config configs/ghibli.yaml`), reading dataset path, trigger phrase, and hyperparameters from that config, and calling shared functions in `data_utils.py` and `logging_utils.py`.
  - Done when: Running `train.py` with any of the three configs executes the same code path, differing only in config values.
5. Add the three adapter configs
  - Files: `configs/ghibli.yaml`, `configs/broadstroke.yaml`, `configs/handsketch.yaml`
  - Execution: Each config specifies the dataset path/identifier, trigger phrase, base model reference (Krea 2), and hyperparameters for that run.
  - Done when: Three config files exist, each pointing at its own dataset and trigger phrase.
6. Add dataset download and caption-editing scripts
  - Files: `scripts/download_data.py`, `scripts/edit_captions.py`
  - Execution: Write a script that downloads each of the three Hugging Face datasets into the git-ignored `data/` folder, and a separate script for reviewing and editing captions before training without altering the original hosted dataset.
  - Done when: Running the download script populates `data/` locally, and captions can be edited independent of the source dataset.
7. Add FAL inference integration
  - Files: `src/inference.py`
  - Execution: Write a module that calls the FAL API for the Krea 2 model to generate test images before, during, and after training runs, for comparing adapter output against the base model.
  - Done when: The script generates a sample image via FAL given a prompt and optional adapter reference.
8. Add RunPod environment setup
  - Files: `requirements.txt`
  - Execution: List the Python dependencies needed on the pod, as boilerplate for now (finalize exact versions once training code is written).
  - Done when: File is committed; dependencies install cleanly from it on a fresh pod (verified later, once `train.py` exists).
9. Add Trackio / Hugging Face Space launch setup
  - Files: `scripts/launch_trackio.py`
  - Execution: Add a boilerplate script to launch Trackio connected to the Hugging Face Space; fill in the actual Space name/config later.
  - Done when: File is committed; Trackio launches and logs to the correct Space once the Space is configured.
10. Commit and push the initial structure to GitHub
  - Files: everything above except `data/` contents
  - Execution: Stage all committed files, commit with a message describing the initial project scaffolding, push to the GitHub remote (`origin`).
  - Done when: The GitHub repo shows the full directory structure with no dataset images or model weights included.



## Out of scope

- Creating and configuring the RunPod pod itself (manual, outside the repo).
- Pulling remote SSH keys and connecting Cursor to the pod.
- Creating the three Hugging Face model repos.
- Actual training runs and pushing trained weights to Hugging Face Hub.
- Git LFS setup (not needed while no large files are committed).



## Risks

- The `requirements.txt` and `scripts/launch_trackio.py` added in Steps 7–8 are boilerplate placeholders; if they aren't revisited once real dependencies/Space config are known, they'll silently drift from what's actually needed.
- If the Trackio/Space launch setup isn't standardized in the repo, tracking configuration could drift between the three training runs.
- If the dataset download script isn't kept separate from caption edits, re-running the download could overwrite edited captions — worth keeping raw and edited captions in distinct files when `scripts/edit_captions.py` is written.

