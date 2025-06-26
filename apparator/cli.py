import argparse
import sys

from apparator.core.browser import with_browsers
from apparator.handlers.hackerrank import HackerRankHandler
from apparator.config import get_config


def list_submissions(args: argparse.Namespace) -> None:
    cfg = get_config()
    with with_browsers(headless=args.headless) as bm:
        page = bm.new_page()
        handler = HackerRankHandler(page, cfg)
        handler.login()
        submissions = handler.list_submissions()
        for idx, sub in enumerate(submissions):
            print(f"[{idx}] {sub['title']} -> {sub['url']}")


def fetch_submission(args: argparse.Namespace) -> None:
    cfg = get_config()
    with with_browsers(headless=args.headless) as bm:
        page = bm.new_page()
        handler = HackerRankHandler(page, cfg)
        handler.login()
        submissions = handler.list_submissions()
        if args.index < 0 or args.index >= len(submissions):
            print("Index out of range", file=sys.stderr)
            return
        entry = submissions[args.index]
        details = handler.fetch_submission(entry, download_dir=args.output)
        print(details["solution"])
        if details.get("pdf"):
            print(f"PDF saved to {details['pdf']}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Interact with HackerRank submissions")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List all submissions")
    list_p.set_defaults(func=list_submissions)

    fetch_p = sub.add_parser("fetch", help="Fetch a submission by index")
    fetch_p.add_argument("index", type=int, help="Index of submission from list")
    fetch_p.add_argument("-o", "--output", default=".", help="Directory to store downloaded PDF")
    fetch_p.set_defaults(func=fetch_submission)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
