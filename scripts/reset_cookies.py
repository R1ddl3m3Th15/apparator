"""Utility script to remove any saved Playwright session data."""
from pathlib import Path
import shutil
from apparator.utils.auth import SESSION_FILE, clear_session


def main() -> None:
    # Remove stored storage_state file
    clear_session()

    # Delete any persistent browser data directories if present
    user_data_dir = Path("playwright")
    if user_data_dir.exists():
        shutil.rmtree(user_data_dir)


if __name__ == "__main__":
    main()
