# apparator/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 1) Figure out where our .env lives (project root)
PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# 2) Load it
load_dotenv(dotenv_path=ENV_PATH)

# 3) Expose the values
HR_USER = os.getenv("HR_USER")
HR_PASS = os.getenv("HR_PASS")
GH_TOKEN = os.getenv("GH_TOKEN")


def get_config() -> dict:
    """
    Returns a dict of all the config values your handlers will need.
    """
    return {
        "HR_USER": HR_USER,
        "HR_PASS": HR_PASS,
        "GH_TOKEN": GH_TOKEN,
    }
