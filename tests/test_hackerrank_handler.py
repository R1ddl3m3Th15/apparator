# tests/test_hackerrank_handler.py
import pytest
pytest.importorskip("playwright")
import os
from apparator.core.browser import with_browsers
from apparator.handlers.hackerrank import HackerRankHandler
from apparator.config import get_config


#@pytest.mark.skip("needs real credentials and is an integration test")
def test_hackerrank_list_submissions():
    config = get_config()
    if not config.get("HR_USER") or not config.get("HR_PASS"):
        pytest.skip("HackerRank credentials not configured")
    with with_browsers(headless=False) as bm:
        page = bm.new_page()
        hr = HackerRankHandler(page, config)
        hr.login()
        subs = hr.list_submissions()
        assert isinstance(subs, list)
        # and at least one entry:
        assert len(subs) > 0
