import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from langdetect import detect
import logging
from deepl import DeepLClient
from pathlib import Path
from .scraper import Scraper

logger = logging.getLogger(__name__)


class PostJobScraper(Scraper):
    def __init__(self, category: str, path: str, deepl_client: DeepLClient, max_pages: int | None = None,
                 delay: float = 2.0):
        super().__init__(category, deepl_client, max_pages, delay)
        self.file_path = path + f'postjob/{self.category}.csv'
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://www.postjobfree.com"
        self.search_url = f'{self.base_url}/resumes?t="{category}"&r=100'

    def _get_resumes_from_page(self, url):
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        resume_links = soup.select("div.snippetPadding h3.itemTitle a")
        resumes = []

        for link in resume_links:
            resume_url = self.base_url + link.get("href")
            try:
                detail_response = requests.get(resume_url, headers=self.headers)
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

                full_resume_div = detail_soup.find("div", class_="normalText")
                if full_resume_div:
                    resume = full_resume_div.get_text(separator="\n", strip=True).replace("Contact this candidate", "")
                    resume_language = detect(resume)
                    if resume_language != "en":
                        resume = self.deepl_client.translate_text(
                            resume, target_lang="EN-US"
                        ).text
                    resumes.append(resume)
                else:
                    logger.warning(f"No full resume found at {resume_url}")
            except Exception as e:
                logger.error(f"Failed to fetch resume at {resume_url}: {e}")

        return resumes

    def scrape(self):
        all_resumes = []
        page = 1

        while True:
            if self.max_pages is not None and page > self.max_pages:
                logger.info(f"Reached max_pages={self.max_pages}. Stopping.")
                break

            page_url = self.search_url + f"&p={page}"
            response = requests.get(page_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            page_resumes = self._get_resumes_from_page(page_url)

            if not page_resumes:
                logger.info(f"No resumes found on page {page}. Stopping.")
                break

            logger.info(f"Scraped page {page}: {len(page_resumes)} resumes found")
            all_resumes.extend(page_resumes)

            header = page == 1
            mode = 'w' if page == 1 else 'a'
            current_df = pd.DataFrame({'Category': self.category, 'Resume': page_resumes})
            current_df.to_csv(self.file_path, index=False, mode=mode, header=header)

            stats_div = soup.select_one("td[style='text-align:right;']")
            if stats_div:
                stats_text = stats_div.get_text(strip=True)
                upper, total = stats_text.replace("Resumes", "").split("of")
                upper = int(upper.split('-')[-1])
                total = int(total)

                if upper >= total:
                    logger.info("Detected last page based on resume count. Stopping.")
                    break

            page += 1
            time.sleep(self.delay)

        logger.info(f"Finished scraping for {self.category}. Total resumes collected: {len(all_resumes)}")
