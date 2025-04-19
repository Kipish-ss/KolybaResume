from abc import ABC, abstractmethod
from deepl import DeepLClient


class BaseScraper(ABC):

    def __init__(self, category: str, file_path: str, deepl_client: DeepLClient, max_pages: int, delay: float):
        self.category = category
        self.file_path = file_path
        self.deepl_client = deepl_client
        self.max_pages = max_pages
        self.delay = delay
        self.headers = {"User-Agent": "Mozilla/5.0"}

    @abstractmethod
    def _get_resumes_from_page(self, url: str) -> list[str]:
        pass

    @abstractmethod
    def scrape(self):
        pass
