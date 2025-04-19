import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from langdetect import detect
import logging
from deepl import DeepLClient
from .scraper import BaseScraper

logger = logging.getLogger(__name__)


class PostJobScraper(BaseScraper):
    def __init__(self, category: str, file_path: str, deepl_client: DeepLClient, max_pages: int | None = None,
                 delay: float = 2.0):
        super().__init__(category, file_path, deepl_client, max_pages, delay)
        self.base_url = "https://www.postjobfree.com"
        self.search_url = f"{self.base_url}/resumes?q=title%3A{category}"

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
            page_resumes = self._get_resumes_from_page(page_url)

            if not page_resumes:
                logger.info(f"No resumes found on page {page}. Stopping.")
                break

            logger.info(f"Page {page} scraped: {len(page_resumes)} resumes")

            all_resumes.extend(page_resumes)

            header = page == 1
            mode = 'w' if page == 1 else 'a'
            current_df = pd.DataFrame({'Category': self.category, 'Resume': page_resumes})
            current_df.to_csv(self.file_path, index=False, mode=mode, header=header)

            page += 1
            time.sleep(self.delay)

        logger.info(f"Scraping complete. Total resumes collected: {len(all_resumes)}")
