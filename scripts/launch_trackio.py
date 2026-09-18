"""Launch Trackio connected to the project's Hugging Face Space.

Usage:
    python scripts/launch_trackio.py
"""

import trackio

TRACKIO_SPACE_ID = "REPLACE_WITH_HF_SPACE_ID"


def launch():
    trackio.init(space_id=TRACKIO_SPACE_ID)


if __name__ == "__main__":
    launch()
