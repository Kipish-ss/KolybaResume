import hashlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from pathlib import Path
from scraper import Scraper

logger = logging.getLogger(__name__)


class PostJobScraper(Scraper):
    def __init__(self, category: str, path: Path, max_pages: int | None = 5,
                 delay: float = 2.0):
        super().__init__(category, max_pages, delay)
        self.file_path = path / 'djinni' / f'{self.category}.csv'
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://www.postjobfree.com"
        self.search_url = f'{self.base_url}/resumes?t="{category}"&r=100'
        self.locations = [
            "", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
            "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
            "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
            "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
            "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
            "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
            "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "District of Columbia",
            "Canada", "India", "United Kingdom", "Germany", "Philippines", "South Africa",
            "Pakistan", "Nigeria", "Australia", "Bangladesh", "Kenya", "United Arab Emirates", "Egypt"
        ]

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

                    resume_hash = hashlib.sha256(resume.encode("utf-8")).hexdigest()

                    if resume_hash not in self.unique_resumes:
                        self.unique_resumes.add(resume_hash)
                        resumes.append(resume)
                else:
                    logger.warning(f"No full resume found at {resume_url}")
            except Exception as e:
                logger.error(f"Failed to fetch resume at {resume_url}: {e}")

        return resumes

    def scrape(self):
        resume_count = 0
        for i, location in enumerate(self.locations):
            url = f"{self.search_url}&l={location}"
            page = 1
            location_resumes = []
            while True:
                if self.max_pages is not None and page > self.max_pages:
                    logger.info(f"Reached max_pages={self.max_pages}. Stopping.")
                    break

                page_url = url + f"&p={page}"
                response = requests.get(page_url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                page_resumes = self._get_resumes_from_page(page_url)

                if not page_resumes:
                    logger.info(f"No resumes found on page {page}. Stopping.")
                    break

                location_resumes.extend(page_resumes)

                stats_div = soup.select_one("td[style='text-align:right;']")
                if stats_div:
                    stats_text = stats_div.get_text(strip=True)
                    upper, total = stats_text.replace("Resumes", "").split("of")
                    upper = int(upper.split('-')[-1])
                    total = int(total)

                    if upper >= total:
                        break

                page += 1
                time.sleep(self.delay)
            header = i == 0
            mode = 'w' if i == 0 else 'a'
            current_df = pd.DataFrame({'Category': self.category, 'Resume': location_resumes})
            current_df.to_csv(self.file_path, index=False, mode=mode, header=header)
            logger.info(f"Scraped location {location or 'Global'}: {len(location_resumes)} resumes found")
            resume_count += len(location_resumes)

            if upper >= total and total <= 500 and i == 0:
                break

        logger.info(f"Finished scraping for {self.category}. Total resumes collected: {resume_count}")