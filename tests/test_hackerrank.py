import importlib.util
import sys
import types
import re


def load_handler():
    """Import HackerRankHandler with a minimal Playwright stub if needed."""
    if importlib.util.find_spec("playwright") is None:
        sync_api = types.ModuleType("playwright.sync_api")
        sync_api.Page = object
        sys.modules.setdefault("playwright", types.ModuleType("playwright"))
        sys.modules["playwright.sync_api"] = sync_api
    from apparator.handlers.hackerrank import HackerRankHandler
    return HackerRankHandler


class DummyElement:
    def __init__(self, text="", href=None, aria=None):
        self._text = text
        self._href = href
        self._aria = aria

    def inner_text(self):
        return self._text

    def get_attribute(self, name):
        if name == "href":
            return self._href
        if name == "aria-disabled":
            return self._aria
        return None

    def query_selector(self, selector):
        return None


class DummyRow:
    def __init__(self, n):
        self._a = DummyElement(text=f"title-{n}", href=f"/url-{n}")
        self._time = DummyElement(text=f"time-{n}")

    def query_selector(self, selector):
        if selector == "a":
            return self._a
        if selector in ("td[aria-label*='Time'], td.submission-time"):
            return self._time
        return None


class DummyPage:
    def __init__(self):
        self.current_page = 0
        self.gotos = []

    def goto(self, url, wait_until=None, timeout=None):
        m = re.search(r"page=(\d+)", url)
        self.current_page = int(m.group(1)) if m else 1
        self.gotos.append(self.current_page)

    def query_selector_all(self, selector):
        if self.current_page > 2:
            return []
        return [DummyRow(self.current_page)]

    def query_selector(self, selector):
        if selector == "li.pagination-next:not(.disabled) a":
            if self.current_page < 2:
                return DummyElement()
            return None
        return None


def test_list_submissions_pagination():
    HackerRankHandler = load_handler()
    page = DummyPage()
    hr = HackerRankHandler(page, {})
    results = hr.list_submissions()
    assert len(results) == 2
    assert page.gotos == [1, 2]

