import time
import logging
from scrapers import DjinniScraper, PostJobScraper



logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
)

DATA_PATH = "ml_backend/data/raw/"
CATEGORIES = [
    "frontend"
    # "backend",
    # "full stack",
    # "devops",
    # "qa"
    # "ux",
    # "designer",
    # "data engineer",
    # "data analyst",
    # "business analyst",
    # "data scientist"
    # "product manager",
    # "project manager",
    # "ios",
    # "android"
    # "marketing",
    # "hr",
    # "recruiter",
    # "seo",
    # "customer support",
    # "c++",
    # "rust",
    # "sales manager",
    # "java",
    # ".net",
    # "python"
    # "software engineer"
]

SCRAPERS = [PostJobScraper]


def main():
    logger.info("Starting scraping process...")
    for ScraperClass in SCRAPERS:
        for category in CATEGORIES:
            logger.info(f"Running {ScraperClass.__name__} for category: {category}")
            scraper = ScraperClass(
                category=category,
                path=DATA_PATH,
            )
            scraper.scrape()
            time.sleep(2)

    logger.info("All scraping jobs completed.")


if __name__ == "__main__":
    main()
