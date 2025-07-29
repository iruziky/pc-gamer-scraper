import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}
response = requests.get(url=url, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')
script_tag = soup.find('script', type='application/json').string

script_json = json.loads(script_tag)
data_str = script_json["props"]["pageProps"]["data"]
data_json = json.loads(data_str)

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

with open("produtos_dict", "w", encoding="utf-8") as arquivo:
    json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
