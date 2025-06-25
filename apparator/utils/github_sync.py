"""Utility helpers for committing files to a Git repository."""

from pathlib import Path
from subprocess import run, CalledProcessError
from typing import Iterable


def commit_files(repo_path: Path, files: Iterable[Path], message: str) -> None:
    """Stage ``files`` inside ``repo_path`` and create a commit."""

    str_files = [str(Path(f)) for f in files]
    try:
        run(["git", "-C", str(repo_path), "add", *str_files], check=True)
        run(["git", "-C", str(repo_path), "commit", "-m", message], check=True)
    except CalledProcessError as exc:
        raise RuntimeError(f"git command failed: {exc}") from exc

