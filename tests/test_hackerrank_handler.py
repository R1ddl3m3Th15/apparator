# tests/test_hackerrank_handler.py
import os
import pytest
from apparator.core.browser import with_browsers
from apparator.handlers.hackerrank import HackerRankHandler
from apparator.config import get_config


#@pytest.mark.skip("needs real credentials and is an integration test")
def test_hackerrank_list_submissions():
    config = get_config()
    with with_browsers(headless=False) as bm:
        page = bm.new_page()
        hr = HackerRankHandler(page, config)
        hr.login()
        subs = hr.list_submissions()
        assert isinstance(subs, list)
        # and at least one entry:
        assert len(subs) > 0
