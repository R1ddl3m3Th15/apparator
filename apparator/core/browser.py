# apparator/core/browser.py
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext
from typing import Optional, Dict


class BrowserManager:
    """
    Context manager that boots up Playwright, launches browsers,
    and shuts everything down cleanly on exit.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless
        self._playwright: Optional[Playwright] = None
        self.browsers: Dict[str, Browser] = {}

    def __enter__(self) -> "BrowserManager":
        # Start Playwright
        self._playwright = sync_playwright().start()
        # Launch 3 engines
        self.browsers["chromium"] = self._playwright.chromium.launch(
            headless=self.headless
        )
        self.browsers["firefox"] = self._playwright.firefox.launch(
            headless=self.headless
        )
        self.browsers["webkit"] = self._playwright.webkit.launch(
            headless=self.headless
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close all browsers
        for browser in self.browsers.values():
            try:
                browser.close()
            except Exception:
                pass
        # Stop Playwright
        if self._playwright:
            self._playwright.stop()

    def new_context(self, engine: str = "chromium", **kwargs) -> BrowserContext:
        """
        Create a fresh browser context (like an incognito profile).
        Pass kwargs through to new_context(), e.g. viewport, user_agent.
        """
        if engine not in self.browsers:
            raise ValueError(
                f"Unknown engine '{engine}'. Choose one of {list(self.browsers)}")
        return self.browsers[engine].new_context(**kwargs)

    def new_page(self, engine: str = "chromium", **kwargs):
        """
        Convenience: open a new context + page in one call.
        """
        ctx = self.new_context(engine, **kwargs)
        return ctx.new_page()


# Convenience function for one-off scripts:
def with_browsers(headless: bool = True):
    """
    Usage:
        with with_browsers(headless=False) as bm:
            page = bm.new_page(engine="firefox")
            page.goto("https://example.com")
    """
    return BrowserManager(headless=headless)
