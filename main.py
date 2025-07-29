import json
from src.scrapers.kabum_scraper import KabumScraper
from src.core.exceptions import *

if __name__ == "__main__":
    scraper = KabumScraper()
    try:
        products_scraped = scraper.run_scraper()

        if products_scraped:
            with open("products_kabum.json", "w", encoding="utf-8") as f:
                json.dump(products_scraped, f, indent=4, ensure_ascii=False)
            print(f"\nScraped {len(products_scraped)} products and saved to 'products_kabum.json'")
        else:
            print("\nNo products were scraped to save.")

    except ScraperNetworkError as e:
        print(f"\n[NETWORK/HTTP ERROR]: {e}")
    except ScraperDataNotFoundError as e:
        print(f"\n[SITE STRUCTURE ERROR]: {e}")
    except ScraperParsingError as e:
        print(f"\n[DATA PARSING ERROR]: {e}")
    except ScraperError as e:
        print(f"\n[GENERAL SCRAPER ERROR]: {e}")
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR]: An unhandled error occurred: {e}")