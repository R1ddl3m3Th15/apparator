# tests/test_browser.py
from apparator.core.browser import with_browsers


def test_launch_and_navigate_hackerrank():
    # Launch in headful mode so Cloudflare is less likely to block us
    with with_browsers(headless=False) as bm:
        page = bm.new_page()
        page.goto(
            "https://www.hackerrank.com/auth/login",
            wait_until="networkidle"
        )
        # Basic check: we're really on the HR login page
        assert page.url.startswith("https://www.hackerrank.com/auth/login")
        # And there should be at least some HTML in the response
        assert len(page.content()) > 100
