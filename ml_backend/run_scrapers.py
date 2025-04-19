from scrapers.djinni_scraper import DjinniScraper
from dotenv import load_dotenv
import os
import logging

load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting all scrapers...")

    scraper = DjinniScraper(
        role_query="backend",
        file_path="ml_backend/data/raw/backend.csv",
        deepl_api_key=DEEPL_API_KEY,
        max_pages=2
    )

    scraper.scrape()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
    )
    main()
