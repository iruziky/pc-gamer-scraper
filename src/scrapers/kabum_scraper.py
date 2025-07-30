import sys
import requests
import json
import time
import logging

from bs4 import BeautifulSoup
from src.core.exceptions import ScraperNetworkError, ScraperDataNotFoundError, ScraperParsingError
from rnet import BlockingClient, Impersonate, RequestError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL_KABUM_GPU = "https://www.kabum.com.br/hardware/placa-de-video-vga"
USER_AGENT_REQUEST = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
PAGE_NOT_FOUND_SELECTOR = "#listingEmpty > b:nth-child(1)"
REQUEST_TIMEOUT = 10

class KabumScraper:
    def __init__(self, category: str):
        """Initializes the scraper with default pagination and request headers."""
        self.category = category
        self.page_number = 1
        self.page_size = 100
        self.client = BlockingClient(
            impersonate=Impersonate.Chrome126,
            timeout=REQUEST_TIMEOUT
        )

    @property
    def url(self):
        """str: The formatted URL for the current page to be scraped."""
        return f'{URL_KABUM_GPU}?page_number={self.page_number}&page_size={self.page_size}'

    def run(self, execute_all_pages: bool = False, execute_main_pages: bool = False):
        """
        Main entry point to run the scraper in a specific mode.

        Args:
            execute_all_pages (bool): If True, scrapes all pages of the category.
            execute_main_pages (bool): If True, scrapes only the first few pages.

        Returns:
            list[dict]: A list of scraped products.
        """
        if execute_all_pages:
            return self._scrape_all_pages()
        elif execute_main_pages:
            return self._scrape_main_pages(num_pages=2)
        else:
            logging.warning("No execution mode was selected. Returning empty list.")
            return []

    def _scrape_all_pages(self):
        """Scraping loop that iterates through all available pages."""
        all_products = []
        while True:
            products_from_page = self._scrape_single_page()
            if not products_from_page:
                break
            all_products.extend(products_from_page)
            self.page_number += 1
            time.sleep(REQUEST_TIMEOUT)
        return all_products

    def _scrape_main_pages(self, num_pages: int = 2):
        """Scraping loop for a limited number of initial pages."""
        all_products = []
        for _ in range(num_pages):
            products_from_page = self._scrape_single_page()
            if not products_from_page:
                break
            all_products.extend(products_from_page)
            self.page_number += 1
            time.sleep(REQUEST_TIMEOUT)
        return all_products
    
    def _scrape_single_page(self):
        """
        Scrapes a single page and returns the products found on it.

        This method performs all the necessary steps for a single page:
        fetching content, parsing HTML, checking for the end of results,
        and extracting the product data from the embedded JSON.

        Returns:
            list[dict] | None:
            A list of product dictionaries from the page,
            or None if the page is empty or the last one.
        """
        response = self._fetch_page_content()
        search_page = BeautifulSoup(response.text(), 'lxml')
        if search_page.select(PAGE_NOT_FOUND_SELECTOR):
            logging.info("No more products found, scraper finished.")
            return None
        
        data_json = self._extract_and_parse_json(search_page)
        logging.info(f"Page {self.page_number} accessed successfully!")
        logging.info(f"Waiting {REQUEST_TIMEOUT} seconds for the next request...")
        return self._get_products(data_json)

    def _fetch_page_content(self):
        """
        Fetches the HTML content for the current page URL.

        It handles network-level errors by wrapping the request in a try-except
        block and raising a custom exception on failure.

        Raises:
            ScraperNetworkError: If the request fails due to a network issue.

        Returns:
            requests.Response: The response object from the successful HTTP GET request.
        """
        try:
            logging.info(f"Fetching URL: {self.url}")
            response = self.client.get(self.url)
            
            if not response.status_code.is_success:
                logging.error(f"Received bad status code: {response.status_code} for URL: {self.url}")
                raise RequestError(f"HTTP Status {response.status_code}")
            return response
        except RequestError as e:
            logging.error(f"Network error on URL: {self.url} - Details: {e}")
            raise ScraperNetworkError(f"Failed to access URL: {self.url}. Details: {e}") from e

    def _extract_and_parse_json(self, search_page):
        """
        Finds, extracts, and parses the embedded JSON data from the page's HTML.

        Args:
            search_page (BeautifulSoup): The parsed HTML content of a search results page.

        Raises:
            ScraperDataNotFoundError: If the specific JSON script tag is not found.
            ScraperParsingError: If the JSON data is malformed or required keys are missing.

        Returns:
            dict: The parsed JSON data containing the product catalog.
        """
        script_tag_element = search_page.find('script', type='application/json')
        if not script_tag_element:
            logging.error("JSON script tag not found on page: %s", self.url)
            raise ScraperDataNotFoundError("JSON script tag not found on the page. Site structure may have changed.")

        try:
            script_tag_content = script_tag_element.string
            script_json = json.loads(script_tag_content)
            data_str = script_json["props"]["pageProps"]["data"]
            data_json = json.loads(data_str)
            return data_json
        except (json.JSONDecodeError, KeyError) as e:
            logging.error("Failed to parse JSON structure. Details: %s", e)
            raise ScraperParsingError(f"Failed to parse JSON data from script. Details: {e}") from e

    def _get_products(self, data_json):
        """
        Processes the raw API data to create a list of product dictionaries.

        Args:
            data_json (dict): The parsed JSON object containing the product catalog.

        Returns:
            list[dict]: A list of cleaned and formatted product dictionaries.
        """
        all_products_data = data_json.get("catalogServer", {}).get("data", [])
        return [
            self._load_product(product)
            for product in all_products_data
        ]
    
    def _load_product(self, product):
        """
        Transforms a single raw product dictionary into a structured, clean format.

        Args:
            product (dict): A dictionary representing a single product from the API.

        Returns:
            dict: A cleaned dictionary with standardized English keys.
        """
        product_dict = {
            "code": product.get("code", "Code Unavailable"),
            "name": product.get("name", "Name Unavailable"),
            "brand": product.get("manufacturer", {}).get("name", "Brand Unavailable"),
            "description": product.get("description", "Description Unavailable"),
            "price": self._get_price(product),
            "image_url": product.get("image", "Image Unavailable"),
            "rating": product.get("rating", "Rating Unavailable"),
            "rating_count": product.get("ratingCount", "Rating Count Unavailable"),
            "warranty": product.get("warranty", "Warranty Unavailable"),
            "isOpenBox": product.get("flags").get("isOpenbox", "Flag Unavailable"),
            "prime_details": product.get("prime").get("priceWithDiscount")
        }
        return product_dict
    
    def _get_price(self, product):
        """
        Retrieves the price of a product using a defined priority logic.

        Args:
            product (dict): A dictionary representing a single product from the API.

        Returns:
            float | str: The product's price, or a string if unavailable.
        """
        price_with_discount = product.get("priceWithDiscount")
        if price_with_discount is not None:
            return price_with_discount

        price_in_offer = product.get("offer")
        if price_in_offer:
            offer_price = price_in_offer.get("priceWithDiscount")
            if offer_price is not None:
                return offer_price

        return product.get("price", "Price Unavailable")