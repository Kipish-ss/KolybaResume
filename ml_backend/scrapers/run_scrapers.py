import time
import logging
from pathlib import Path
import os
from djinni_scraper import DjinniScraper
from postjob_scraper import PostJobScraper

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
)

script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
ml_backend_dir = script_dir.parent
DATA_PATH = ml_backend_dir / "data" / "raw"

CATEGORIES = [
    "frontend",
    "backend",
    "full stack",
    "devops",
    "qa engineer",
    "ux",
    "designer",
    "data engineer",
    "data analyst",
    "business analyst",
    "data scientist",
    "product manager",
    "project manager",
    "ios",
    "android",
    "flutter",
    "marketing",
    "hr",
    "recruiter",
    "seo",
    "customer support",
    "c++",
    "rust",
    "sales manager",
    "java",
    ".net",
    "python",
    "software engineer"
]

SCRAPERS = [DjinniScraper, PostJobScraper]


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
