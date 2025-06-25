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
        self.page.wait_for_url(
            "https://www.hackerrank.com/dashboard", timeout=20000)

    def list_submissions(self) -> List[Dict[str, Any]]:
        """
        Visit the global all-submissions page and collect entries.
        """
        self.page.goto(
            "https://www.hackerrank.com/submissions/all",
            wait_until="domcontentloaded",
            timeout=60000
        )
        items = self.page.query_selector_all(".submissions-list-item")
        results: List[Dict[str, Any]] = []
        for itm in items:
            link = itm.query_selector("a.challenge-link").get_attribute("href")
            title = itm.query_selector(".challenge-name").inner_text()
            results.append({"title": title, "url": link})
        return results

    def fetch_submission(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Given a submission entry, navigate to its page and extract details.
        """
        self.page.goto(
            entry["url"],
            wait_until="domcontentloaded",
            timeout=60000
        )
        title = self.page.query_selector(".challenge-heading").inner_text()
        statement = self.page.query_selector(
            ".challenge-description"
        ).inner_text()
        code = self.page.query_selector(
            ".editor-content"
        ).inner_text()
        return {
            "title": title,
            "statement": statement,
            "solution": code
        }
