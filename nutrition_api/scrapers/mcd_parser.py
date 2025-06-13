import os
import json
import logging
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Constants ---
URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"
BASE_URL = "https://www.mcdonalds.com/ua/uk-ua/product/{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0"}
JSON_FILE = os.path.join(os.path.dirname(__file__), "..", "storage", "mcd_products.json")
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
# --- Selenium options ---
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # Important for Docker
# --- Logging ---
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(asctime)s]: %(message)s")
# --- Cache ---
_cached_product_ids = None


def get_product_ids():
    global _cached_product_ids
    if _cached_product_ids:
        return _cached_product_ids

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    product_ids = []
    product_id_name_map = []

    for li in soup.select("li.cmp-category__item"):
        prod_id = li.get("data-product-id", "unknown")
        name_el = li.select_one(".cmp-category__item-name")
        prod_name = name_el.get_text(strip=True) if name_el else "unknown"
        product_ids.append(prod_id)
        product_id_name_map.append({"id": prod_id, "name": prod_name})

    _cached_product_ids = (product_ids, product_id_name_map)
    logger.info(f"Retrieved {len(product_ids)} product IDs.")
    return _cached_product_ids


def get_product_html(product_id, driver):
    cache_path = os.path.join(CACHE_DIR, f"{product_id}.html")

    if os.path.exists(cache_path):
        logger.debug(f"Loading cached HTML for product {product_id}")
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    try:
        logger.info(f"Fetching HTML for product {product_id}")
        driver.get(BASE_URL.format(product_id))
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.cmp-product-details-main__heading-title"))
        )
        html = driver.page_source
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)
        return html
    except Exception as e:
        logger.warning(f"Failed to fetch HTML for product {product_id}: {e}")
        return None


def parse_product_html(html):
    soup = BeautifulSoup(html, "html.parser")

    def safe_text(selector):
        el = soup.select_one(selector)
        return el.text.strip() if el else None

    name = safe_text("span.cmp-product-details-main__heading-title")
    description = safe_text("div.cmp-product-details-main__description div.cmp-text")

    if not name:
        raise ValueError("Product name not found in HTML")

    nutrition_map = {
        "calories": None, "fats": None, "carbs": None,
        "proteins": None, "unsaturated fats": None,
        "sugar": None, "salt": None, "portion": None
    }

    for item in soup.select("li.cmp-nutrition-summary__heading-primary-item"):
        metric = item.select_one("span.metric span[aria-hidden='true']")
        value = item.select_one("span.value span[aria-hidden='true']")
        if metric and value:
            key = metric.get_text(strip=True).lower()
            val = value.get_text(strip=True)
            if "калор" in key:
                nutrition_map["calories"] = val
            elif "жири" in key:
                nutrition_map["fats"] = val
            elif "вуглеводи" in key:
                nutrition_map["carbs"] = val
            elif "білки" in key:
                nutrition_map["proteins"] = val
            elif "порція" in key:
                nutrition_map["portion"] = val

    for item in soup.select("li.label-item"):
        metric = item.select_one("span.metric")
        value = item.select_one("span.value span[aria-hidden='true']")
        if metric and value:
            key = metric.get_text(strip=True).lower().replace(":", "")
            val = value.get_text(strip=True).split('\n')[0]
            if "нжк" in key or "ненасичені" in key:
                nutrition_map["unsaturated fats"] = val
            elif "цукор" in key:
                nutrition_map["sugar"] = val
            elif "сіль" in key:
                nutrition_map["salt"] = val
            elif "порція" in key:
                nutrition_map["portion"] = val

    return {
        "name": name,
        "description": description,
        **nutrition_map
    }


def fetch_product_data(product_id, driver):
    html = get_product_html(product_id, driver)
    if not html:
        return None
    try:
        return parse_product_html(html)
    except Exception as e:
        logger.error(f"Failed to parse product {product_id}: {e}")
        return None


def save_all_products():
    from .mcd_parser import get_product_ids, fetch_product_data
    from selenium import webdriver

    product_ids, _ = get_product_ids()
    driver = webdriver.Chrome(options=options)

    result = []
    try:
        for pid in product_ids:
            data = fetch_product_data(pid, driver)
            if data:
                result.append(data)
                logger.info(f"Successfully parsed product {pid}")
            else:
                logger.warning(f"No data for product {pid}")
    finally:
        driver.quit()

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(result)} products to {JSON_FILE}")
