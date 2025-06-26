# apparator/handlers/hackerrank.py

from apparator.core.handler_base import SiteHandler
from playwright.sync_api import Page
from typing import List, Dict, Any


class HackerRankHandler(SiteHandler):
    def __init__(self, page: Page, config: Dict[str, Any]):
        super().__init__(page, config)
        self.username = config.get("HR_USER")
        self.password = config.get("HR_PASS")

    def login(self) -> None:
        """
        Navigate to the login page and authenticate the user.
        """
        # Load login page (wait for DOM content)
        self.page.goto(
            "https://www.hackerrank.com/auth/login",
            wait_until="domcontentloaded",
            timeout=60000
        )
        # Fill credentials
        self.page.fill("input[name='username']", self.username)
        self.page.fill("input[name='password']", self.password)
        # Click the submit button
        self.page.click("button[type=submit]")
        # Wait until redirected to dashboard
        # allow more time here in case the redirect takes a while
        self.page.wait_for_url(
            "https://www.hackerrank.com/dashboard", timeout=60000)

    def list_submissions(self) -> List[Dict[str, Any]]:
        """Return a list of all submissions across every page."""

        page_num = 1
        results: List[Dict[str, Any]] = []

        while True:
            self.page.goto(
                f"https://www.hackerrank.com/submissions/all?page={page_num}",
                wait_until="domcontentloaded",
                timeout=60000,
            )

            items = self.page.query_selector_all(".submissions-list-item")
            if not items:
                break

            for itm in items:
                link_el = itm.query_selector("a.challenge-link")
                if not link_el:
                    continue
                link = link_el.get_attribute("href")
                title = itm.query_selector(".challenge-name").inner_text().strip()
                time_el = itm.query_selector(".submission-time")
                timestamp = time_el.inner_text().strip() if time_el else ""
                results.append({
                    "title": title,
                    "url": link,
                    "timestamp": timestamp,
                })

            next_btn = self.page.query_selector("li.pagination-next:not(.disabled) a")
            if not next_btn:
                break
            page_num += 1

        return results

    def fetch_submission(self, entry: Dict[str, Any], download_dir: str = "") -> Dict[str, Any]:
        """Download the submission details and problem statement PDF."""

        self.page.goto(
            entry["url"],
            wait_until="domcontentloaded",
            timeout=60000,
        )

        title = self.page.query_selector(".challenge-heading").inner_text().strip()
        statement = self.page.query_selector(".challenge-description").inner_text()
        code = self.page.query_selector(".editor-content").inner_text()

        pdf_path = None
        if download_dir:
            self.page.wait_for_selector("a:has-text('Download Problem Statement')")
            with self.page.expect_download() as dl_info:
                self.page.click("a:has-text('Download Problem Statement')")
            download = dl_info.value
            pdf_path = f"{download_dir}/{title}.pdf"
            download.save_as(pdf_path)

        return {
            "title": title,
            "statement": statement,
            "solution": code,
            "pdf": pdf_path,
        }
