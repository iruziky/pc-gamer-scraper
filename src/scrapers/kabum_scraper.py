import requests
import json
from bs4 import BeautifulSoup

class KabumScraper:
    def __init__(self):
        self.url = 'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

    def run_scraper(self):
        request = self.get_url()

        search_page = BeautifulSoup(request.text, 'lxml')
        
        script_element = search_page.find('script', type='application/json')
        if not script_element:
            print("Erro: Script JSON da página não encontrado. Verifique a estrutura do site.")
            return []
        
        script_str = script_element.string
        
        if not script_str:
            print("Erro: Script JSON da página não encontrado. Verifique a estrutura do site.")
            return []

        script_json = json.loads(script_str)
        data_str = script_json["props"]["pageProps"]["data"]
        data_json = json.loads(data_str)
        
        produtos = self.get_products(data_json)
        return produtos
    
    def get_url(self):
        response = requests.get(url=self.url, headers=self.headers)
        response.raise_for_status()
        return response
    
    def get_products(self, data_json):
        produtos = list()
        for produto in data_json["catalogServer"]["data"]:
            name = produto.get("name", "Nome Indisponível")
            price = produto.get("price")

            if produto.get("priceWithDiscount") is not None:
                price = produto["priceWithDiscount"]

            offer_data = produto.get("offer")
            if offer_data and offer_data.get("priceWithDiscount") is not None:
                price = offer_data["priceWithDiscount"]

            produto_dict = {
                "nome": name.replace(" ", ""),
                "preco": (int)(price)
            }

            produtos.append(produto_dict)

        return produtos