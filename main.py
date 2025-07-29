# main.py

import json
import logging
import argparse
from src.scrapers.kabum_scraper import KabumScraper
from src.core.exceptions import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to parse arguments and run the scraper.
    """
    parser = argparse.ArgumentParser(description="Scrape product data from Kabum!.")
    
    parser.add_argument(
        "mode", 
        type=str,
        choices=['all_pages', 'main_pages'],
        help="The scraping mode: 'all_pages' to scrape everything, or 'main_pages' for the first few pages."
    )
    
    parser.add_argument(
        "category",
        type=str,
        help="The category slug to scrape (e.g., 'hardware/processadores')."
    )

    args = parser.parse_args()
    
    try:
        scraper = KabumScraper(category=args.category)
        products_scraped = []
        
        if args.mode == 'all_pages':
            logging.info(f"Starting scraper in FULL mode for category: {args.category}")
            products_scraped = scraper.run(execute_all_pages=True)
            output_filename = f"products_kabum_{args.category.replace('/', '_')}_all.json"
            
        elif args.mode == 'main_pages':
            logging.info(f"Starting scraper in MAIN PAGES mode for category: {args.category}")
            products_scraped = scraper.run(execute_main_pages=True)
            output_filename = f"products_kabum_{args.category.replace('/', '_')}_main.json"

        if products_scraped:
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(products_scraped, f, indent=4, ensure_ascii=False)
            logging.info(f"Scraped {len(products_scraped)} products and saved to '{output_filename}'")
        else:
            logging.warning("No products were scraped.")

    except ScraperNetworkError as e:
        logging.critical(f"[NETWORK/HTTP ERROR]: {e}")
    except ScraperDataNotFoundError as e:
        logging.critical(f"[SITE STRUCTURE ERROR]: {e}")
    except ScraperParsingError as e:
        logging.critical(f"[DATA PARSING ERROR]: {e}")
    except Exception as e:
        logging.exception("[UNEXPECTED ERROR]: An unhandled error occurred.")


if __name__ == "__main__":
    main()