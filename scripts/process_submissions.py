"""Example script to process new HackerRank submissions."""

import argparse
import json
from pathlib import Path

from apparator.core.browser import with_browsers
from apparator.handlers.hackerrank import HackerRankHandler
from apparator.config import get_config
from apparator.utils.github_sync import commit_files


STATE_FILE = Path("submissions.json")
PROBLEMS_DIR = Path("problems")


def load_state() -> list:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return []


def save_state(data: list) -> None:
    STATE_FILE.write_text(json.dumps(data, indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Process new HackerRank submissions")
    parser.add_argument("--repo", default=".", help="Path to git repository for commits")
    parser.add_argument("--headless", action="store_true", help="Run browser headless")
    args = parser.parse_args(argv)

    cfg = get_config()
    known = load_state()
    known_urls = {e["url"] for e in known}

    with with_browsers(headless=args.headless) as bm:
        page = bm.new_page()
        hr = HackerRankHandler(page, cfg)
        hr.login()
        submissions = hr.list_submissions()

        new_entries = [s for s in submissions if s["url"] not in known_urls]
        for entry in new_entries:
            folder = PROBLEMS_DIR / entry["title"].replace(" ", "_")
            folder.mkdir(parents=True, exist_ok=True)
            details = hr.fetch_submission(entry, download_dir=str(folder))
            (folder / "solution.txt").write_text(details["solution"])
            if details.get("pdf"):
                commit_files(Path(args.repo), [folder], f"Add {entry['title']}")

        save_state(submissions)


if __name__ == "__main__":
    main()

