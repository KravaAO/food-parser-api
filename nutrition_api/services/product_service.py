import os
import json
from nutrition_api.scrapers.mcd_parser import get_product_ids, fetch_product_data, save_all_products
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

JSON_FILE = os.path.join(os.path.dirname(__file__), "..", "storage", "mcd_products.json")
# --- Selenium options ---
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

def load_all_products():
    save_all_products()
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_or_update_product_to_json(product_data):
    products = load_all_products()

    updated = False
    for i, p in enumerate(products):
        if p["name"].lower() == product_data["name"].lower():
            products[i] = product_data
            updated = True
            break

    if not updated:
        products.append(product_data)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def get_product_by_name(name: str):
    product_ids, product_map = get_product_ids()
    name_to_id = {item["name"].lower(): item["id"] for item in product_map}
    product_id = name_to_id.get(name.lower())
    if not product_id:
        return None

    driver = webdriver.Chrome(options=options)
    try:
        data = fetch_product_data(product_id, driver)
        if data:
            save_or_update_product_to_json(data)
        return data
    finally:
        driver.quit()

def get_product_field(name: str, field: str):
    product = get_product_by_name(name)
    if product:
        return product.get(field)
    return None
