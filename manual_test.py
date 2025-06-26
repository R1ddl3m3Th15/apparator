# manual_test.py
import pytest
pytest.importorskip("playwright")
from apparator.core.browser import with_browsers
from apparator.handlers.hackerrank import HackerRankHandler
from apparator.config import get_config


def main():
    cfg = get_config()
    with with_browsers(headless=False) as bm:
        page = bm.new_page()
        print("→ Logging in…")
        hr = HackerRankHandler(page, cfg)
        hr.login()
        print("→ Listing submissions…")
        subs = hr.list_submissions()
        print(f"→ Found {len(subs)} submissions:")
        for s in subs[:5]:
            print("   •", s["title"], "→", s["url"])

        if subs:
            print("→ Fetching first submission…")
            details = hr.fetch_submission(subs[0], download_dir=".")
            print("Downloaded:", details.get("pdf"))


if __name__ == "__main__":
    main()
