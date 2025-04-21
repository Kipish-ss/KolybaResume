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
    def __init__(self, category: str, path: str, max_pages: int | None = None,
                 delay: float = 2.0):
        super().__init__(category, max_pages, delay)
        self.file_path = path + f'djinni/{self.category}.csv'
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://djinni.co"
        self.search_url = f"{self.base_url}/developers/?keywords={category}&options=skip_skills"

    def _get_resumes_from_page(self, url):
        response = requests.get(url, headers=self.headers)
        while response.text.startswith("Your IP address"):
            logger.warning("Blocked by Djinni. Change VPN location.")
            time.sleep(1)
            input("Press any key to continue...")
            response = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        resume_divs = soup.find_all("div", class_="text-card")

        resumes = []
        for resume_div in resume_divs:
            resume = resume_div.get_text(separator="\n", strip=True)

            resume_hash = hashlib.sha256(resume.encode("utf-8")).hexdigest()
            resumes.append(resume_hash)
            if resume_hash not in self.unique_resumes:
                self.unique_resumes.add(resume_hash)
                resumes.append(resume)
            resumes.append(resume)

        return resumes

    def scrape(self):
        all_resumes = []
        page = 1

        while True:
            if self.max_pages is not None and page > self.max_pages:
                logger.info(f"Reached max_pages={self.max_pages}. Stopping.")
                break

            url = f"{self.search_url}&page={page}"
            page_resumes = self._get_resumes_from_page(url)

            if not page_resumes:
                logger.info(f"No resumes found on page {page}. Stopping.")
                break

            logger.info(f"Scraped page {page}: {len(page_resumes)} resumes found")

            all_resumes.extend(page_resumes)

            header = page == 1
            mode = 'w' if page == 1 else 'a'
            current_df = pd.DataFrame({'Category': self.category, 'Resume': page_resumes})
            current_df.to_csv(self.file_path, index=False, mode=mode, header=header)

            page += 1
            time.sleep(self.delay)

        logger.info(f"Finished scraping for {self.category}. Total resumes collected: {len(all_resumes)}")
