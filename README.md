# Apparator

Apparator is a small prototype for programmatically collecting coding challenge submissions. It uses [Playwright](https://playwright.dev/) to drive a browser and log in to sites such as HackerRank. Site specific logic lives in "handler" classes that implement a common interface. The included `HackerRankHandler` shows how to log in, list submissions and fetch individual solutions.

The `BrowserManager` context in `apparator/core/browser.py` manages launching Chromium, Firefox and WebKit instances. Handler classes derive from `SiteHandler` in `apparator/core/handler_base.py` which defines the basic workflow of `login`, `list_submissions` and `fetch_submission`.

## Required configuration

Credentials and tokens are loaded from a `.env` file at the project root. Use `config/.env.example` as a template:

```dotenv
# HackerRank credentials
HR_USER=your_hackerrank_username
HR_PASS=your_hackerrank_password

# GitHub token (with repo scope)
GH_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXX
```

At runtime the values are accessed in `apparator/config.py` as `HR_USER`, `HR_PASS` and `GH_TOKEN`.

## Installation

Create a virtual environment and install dependencies:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
playwright install
```

## Running the scripts

After setting up your `.env` file you can run one of the provided scripts:

* `scripts/process_submissions.py` – download new submissions and commit them to a Git repository. Use `--repo` to specify the target repo and `--headless` to run the browser without a UI.
* `manual_test.py` – simple demo that logs in and prints the first few submissions.

Examples:

```bash
python manual_test.py
```

Process and commit new submissions to a repository:

```bash
python scripts/process_submissions.py --repo /path/to/repo --headless
```

Both scripts expect the environment variables shown above to be present.

## Command line interface

`apparator/cli.py` provides a simple command line wrapper around
`HackerRankHandler`. Use it to list your submissions or download a single
submission by its index.

List all submissions:

```bash
python -m apparator.cli list
```

Fetch a submission (use the index printed by the list command):

```bash
python -m apparator.cli fetch 0
```

Run with `-h` to see all options including `--headless` and the output
directory for downloaded PDFs.
