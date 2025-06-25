# apparator/core/handler_base.py

from abc import ABC, abstractmethod
from playwright.sync_api import Page
from typing import List, Dict, Any


class SiteHandler(ABC):
    """
    Base class for coding‐platform handlers.
    Each handler must know how to:
      1. login()
      2. list_submissions() → returns a list of metadata dicts
      3. fetch_submission(entry) → navigates page and returns full details
    """

    def __init__(self, page: Page, config: Dict[str, Any]):
        """
        :param page: a Playwright Page instance (fresh context)
        :param config: dict loaded from your .env or config.py
        """
        self.page = page
        self.config = config

    @abstractmethod
    def login(self) -> None:
        """Perform whatever steps are needed to log in."""
        pass

    @abstractmethod
    def list_submissions(self) -> List[Dict[str, Any]]:
        """
        Return a list of “entries,” e.g.
        [
          {"title": "...", "url": "...", "timestamp": "...", ...},
          ...
        ]
        """
        pass

    @abstractmethod
    def fetch_submission(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Given one metadata entry from list_submissions(),
        navigate/fetch the problem statement + code + any other info,
        and return it in a structured dict.
        """
        pass
