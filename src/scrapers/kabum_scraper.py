import requests
import json
from bs4 import BeautifulSoup

from src.core.exceptions import *

class KabumScraper:
    def __init__(self):
        self.url = 'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

    def run_scraper(self):
        response = self._fetch_page_content()
        data_json = self._extract_and_parse_json(response.text)
        
        produtos = self.get_products(data_json)
        return produtos

    def _fetch_page_content(self):
        """Fetches the page content and handles network errors."""
        try:
            response = requests.get(url=self.url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise ScraperNetworkError(f"Failed to access URL: {self.url}. Details: {e}") from e

    def _extract_and_parse_json(self, html_content):
        """Extracts and parses the embedded JSON data from the HTML."""
        search_page = BeautifulSoup(html_content, 'lxml')

        script_tag_element = search_page.find('script', type='application/json')
        if not script_tag_element:
            raise ScraperDataNotFoundError("JSON script tag not found on the page. Site structure may have changed.")

        try:
            script_tag_content = script_tag_element.string
            script_json = json.loads(script_tag_content)
            data_str = script_json["props"]["pageProps"]["data"]
            data_json = json.loads(data_str)
            return data_json
        except (json.JSONDecodeError, KeyError) as e:
            raise ScraperParsingError(f"Failed to parse JSON data from script. Details: {e}") from e

    def get_products(self, data_json):
        produtos = []
        for produto in data_json.get("catalogServer", {}).get("data", []):
            name = produto.get("name", "Nome Indisponível")
            price = produto.get("price", "Preço Indisponível")

            offer_data = produto.get("offer")
            if offer_data and offer_data.get("priceWithDiscount") is not None:
                price = offer_data["priceWithDiscount"]
            elif produto.get("priceWithDiscount") is not None:
                price = produto["priceWithDiscount"]

            produto_dict = {
                "nome": name,
                "preco": price
            }

            produtos.append(produto_dict)

        return produtos