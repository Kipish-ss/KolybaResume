import requests
from .scraper import Scraper
from bs4 import BeautifulSoup
import pandas as pd
import time
import hashlib
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DjinniScraper(Scraper):
    def __init__(self, category: str, path: Path, max_pages: int | None = None,
                 delay: float = 2.0):
        super().__init__(category, max_pages, delay)
        self.file_path = path / 'djinni' / f'{self.category}.csv'
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://djinni.co"
        if category in ["frontend", "backend"]:
            self.search_url = f'{self.base_url}/developers/?keywords="{category}"-full&options=skip_skills'
        elif category == "c++":
            self.search_url = f'{self.base_url}/developers/?keywords="c%2B%2B"&options=skip_skills'
        else:
            self.search_url = f'{self.base_url}/developers/?keywords="{category}"&options=skip_skills'

    def get_total_pages(self) -> int:
        url = self.search_url
        response = requests.get(url, headers=self.headers)
        if response.text.startswith("Your IP address"):
            logger.warning("Blocked by Djinni. Change VPN location.")
            time.sleep(1)
            input("Press any key to continue...")
            response = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        pagination = soup.find("ul", class_="pagination")
        if pagination:
            page_links = pagination.find_all("a", class_="page-link")
            page_numbers = []
            for link in page_links:
                try:
                    text = link.text.strip()
                    if text.isdigit():
                        page_numbers.append(int(text))
                except ValueError:
                    continue

            if page_numbers:
                total_pages = max(page_numbers)
                logger.info(f"Detected {total_pages} total pages for category: {self.category}")
                return total_pages

        logger.warning("Could not determine total pages, assuming single page")
        return 1

    def _get_resumes_from_page(self, url, max_retries=3):
        retries = 0
        while retries < max_retries:
            response = requests.get(url, headers=self.headers)

            if response.text.startswith("Your IP address"):
                logger.warning("Blocked by Djinni. Change VPN location.")
                time.sleep(1)
                input("Press ENTER to continue...")
                time.sleep(5)
                retries += 1
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            resume_divs = soup.find_all("div", class_="text-card")

            if resume_divs:
                resumes = []
                for resume_div in resume_divs:
                    resume = resume_div.get_text(separator="\n", strip=True)
                    resume_hash = hashlib.sha256(resume.encode("utf-8")).hexdigest()
                    if resume_hash not in self.unique_resumes:
                        self.unique_resumes.add(resume_hash)
                        resumes.append(resume)

                return resumes
            else:
                logger.warning(f"No resume divs found on page, retry {retries + 1}/{max_retries}")

                if "detected" in response.text.lower() or "suspicious" in response.text.lower():
                    logger.warning("Possible undetected block. Waiting for user input...")
                    input("Press ENTER to continue after changing VPN...")

                retries += 1
                time.sleep(5)

        logger.error(f"Failed to get resumes after {max_retries} retries")
        return []

    def scrape(self):
        all_resumes = []
        total_pages = self.get_total_pages()

        for page in range(1, total_pages + 1):
            if self.max_pages is not None and page > self.max_pages:
                logger.info(f"Reached max_pages={self.max_pages}. Stopping.")
                break

            url = f"{self.search_url}&page={page}"
            page_resumes = self._get_resumes_from_page(url)

            logger.info(f"Scraped page {page}: {len(page_resumes)} resumes found")

            all_resumes.extend(page_resumes)

            header = page == 1
            mode = 'w' if page == 1 else 'a'
            current_df = pd.DataFrame({'Category': self.category, 'Resume': page_resumes})
            current_df.to_csv(self.file_path, index=False, mode=mode, header=header)

            time.sleep(self.delay)

        logger.info(f"Finished scraping for {self.category}. Total resumes collected: {len(all_resumes)}")
