from deepl import DeepLClient
from scrapers import DjinniScraper
from scrapers import PostJobScraper
from dotenv import load_dotenv
import os
import logging

load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
deepl_client = DeepLClient(DEEPL_API_KEY)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting all scrapers...")

    # scraper = DjinniScraper(
    #     role_query="backend",
    #     file_path="ml_backend/data/raw/djinni_backend.csv",
    #     deepl_client=deepl_client,
    #     max_pages=2
    # )

    scraper = PostJobScraper(
        category="backend",
        file_path="ml_backend/data/raw/post_backend.csv",
        deepl_client=deepl_client,
        max_pages=10
    )

    scraper.scrape()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
    )
    main()
