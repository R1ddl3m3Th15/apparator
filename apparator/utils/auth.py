from __future__ import annotations
import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
SESSION_FILE = PROJECT_ROOT / "playwright_state.json"


def load_credentials(env_path: Path = ENV_FILE) -> Dict[str, str]:
    """Load credentials from environment or a ``.env`` file."""
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    return {
        "HR_USER": os.getenv("HR_USER", ""),
        "HR_PASS": os.getenv("HR_PASS", ""),
        "GH_TOKEN": os.getenv("GH_TOKEN", ""),
    }


def load_session(browser: Browser, storage_path: Path = SESSION_FILE, **kwargs) -> BrowserContext:
    """Return a new context using saved Playwright storage if available."""
    if storage_path.exists():
        return browser.new_context(storage_state=str(storage_path), **kwargs)
    return browser.new_context(**kwargs)


def save_session(context: BrowserContext, storage_path: Path = SESSION_FILE) -> None:
    """Persist the given context's storage state."""
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(storage_path))


def clear_session(storage_path: Path = SESSION_FILE) -> None:
    """Remove any saved storage state."""
    if storage_path.exists():
        storage_path.unlink()
