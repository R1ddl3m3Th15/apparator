import importlib.util
import sys
import types
import re


def load_handler():
    """Import HackerRankHandler with a minimal Playwright stub if needed."""
    try:
        spec = importlib.util.find_spec("playwright")
    except ValueError:
        spec = None
    if spec is None and "playwright" not in sys.modules:
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


class DummyDownload:
    def __init__(self):
        self.saved_to = None

    def save_as(self, path):
        self.saved_to = path


class DummyFetchPage:
    def __init__(self):
        self.goto_urls = []
        self.clicked = []
        self.waited = []
        self.selectors = {}
        self.download = DummyDownload()

    def goto(self, url, wait_until=None, timeout=None):
        self.goto_urls.append(url)

    def query_selector(self, selector):
        return self.selectors.get(selector)

    def wait_for_selector(self, selector):
        self.waited.append(selector)

    def click(self, selector):
        self.clicked.append(selector)

    def expect_download(self):
        page = self

        class Ctx:
            def __enter__(self_inner):
                return self_inner

            def __exit__(self_inner, exc_type, exc_val, exc_tb):
                pass

            @property
            def value(self_inner):
                return page.download

        return Ctx()


def make_fetch_page():
    page = DummyFetchPage()
    page.selectors[".challenge-heading"] = DummyElement("Challenge")
    page.selectors[".challenge-description"] = DummyElement("Statement")
    page.selectors[".editor-content"] = DummyElement("print('hi')")
    return page


def test_fetch_submission_no_download():
    HackerRankHandler = load_handler()
    page = make_fetch_page()
    hr = HackerRankHandler(page, {})
    result = hr.fetch_submission({"url": "https://example.com"})
    assert result == {
        "title": "Challenge",
        "statement": "Statement",
        "solution": "print('hi')",
        "pdf": None,
    }
    assert page.goto_urls == ["https://example.com"]


def test_fetch_submission_download_pdf(tmp_path):
    HackerRankHandler = load_handler()
    page = make_fetch_page()
    hr = HackerRankHandler(page, {})
    result = hr.fetch_submission({"url": "https://example.com"}, download_dir=str(tmp_path))
    expected_pdf = str(tmp_path / "Challenge.pdf")
    assert result["pdf"] == expected_pdf
    assert page.download.saved_to == expected_pdf
    assert page.waited == ["a:has-text('Download Problem Statement')"]
    assert page.clicked == ["a:has-text('Download Problem Statement')"]

