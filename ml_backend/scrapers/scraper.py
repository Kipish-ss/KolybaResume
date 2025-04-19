from abc import ABC, abstractmethod


class BaseScraper(ABC):

    def __init__(self, role_query: str, file_path: str, max_pages: int, delay: float):
        self.role_query = role_query
        self.file_path = file_path
        self.max_pages = max_pages
        self.delay = delay

    @abstractmethod
    def _get_resumes_from_page(self, url: str) -> list[str]:
        pass

    @abstractmethod
    def scrape(self):
        pass
