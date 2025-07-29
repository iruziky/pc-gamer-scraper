import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

url = 'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100'

PRODUCT_CARD_SELECTOR = "div.p-\[2px\]"
NAME_RELATIVE_SELECTOR = "article > a:nth-child(2) > div:nth-child(2) > button:nth-child(2) > div:nth-child(1) > h3:nth-child(1) > span:nth-child(1)"
PRICE_RELATIVE_SELECTOR = "article:nth-child(1) > a:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > span:nth-child(1)"

print("Iniciando o navegador (Selenium Undetected)...")
options = uc.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = uc.Chrome(options=options)
except Exception as e:
    print(f"Erro ao iniciar o Chrome com undetected_chromedriver: {e}")
    print("Tentando com caminho padrão ou sem cache.")
    driver = uc.Chrome(options=options, use_custom_user_agent=True)

driver.get(url)

try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCT_CARD_SELECTOR))
    )
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    

except Exception as e:
    print(f"Erro ao esperar pelos produtos ou rolar a página: {e}")
    driver.quit()
    exit()

scraped_data_selenium = []
try:
    product_elements = driver.find_elements(By.CSS_SELECTOR, PRODUCT_CARD_SELECTOR)

    print(f"Encontrados {len(product_elements)} elementos de produto na página.")

    for i, product_element in enumerate(product_elements):
        try:
            name_element = product_element.find_element(By.CSS_SELECTOR, NAME_RELATIVE_SELECTOR)
            price_element = product_element.find_element(By.CSS_SELECTOR, PRICE_RELATIVE_SELECTOR)

            name = name_element.text.strip()
            price_text = price_element.text.strip().replace("R$", "").replace(".", "").replace(",", ".").strip()
            
            try:
                price = float(price_text)
            except ValueError:
                price = price_text

            scraped_data_selenium.append({"nome": name.replace(" ", ""), "preco": (int)(price)})

        except Exception as e:
            continue

except Exception as e:
    print(f"Erro ao encontrar contêineres de produto com o seletor '{PRODUCT_CARD_SELECTOR}': {e}")

finally:
    driver.quit()

print(f"Total de produtos coletados pelo Selenium: {len(scraped_data_selenium)}")

output_file = "kabum_selenium_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(scraped_data_selenium, f, ensure_ascii=False, indent=4)

print(f"\nDados do Selenium salvos em '{output_file}'")