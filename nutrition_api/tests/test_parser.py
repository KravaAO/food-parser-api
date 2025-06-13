import os
import pytest
from unittest.mock import MagicMock, patch
from nutrition_api.scrapers import mcd_parser


def test_get_product_ids_structure():
    product_ids, product_map = mcd_parser.get_product_ids()
    assert isinstance(product_ids, list)
    assert isinstance(product_map, list)
    assert all("id" in p and "name" in p for p in product_map)


@patch("selenium.webdriver.Chrome")
def test_fetch_product_data_from_cache(mock_webdriver, tmp_path):
    product_id = "12345"
    html_content = """
    <html>
        <span class="cmp-product-details-main__heading-title">Біг-Мак</span>
        <div class="cmp-product-details-main__description">
            <div class="cmp-text"><p>Опис продукту</p></div>
        </div>
    </html>
    """
    cache_dir = os.path.join(tmp_path, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    file_path = os.path.join(cache_dir, f"{product_id}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    original_cache_dir = mcd_parser.CACHE_DIR
    mcd_parser.CACHE_DIR = cache_dir

    result = mcd_parser.fetch_product_data(product_id, MagicMock())

    assert result["name"] == "Біг-Мак"
    assert "Опис" in result["description"]

    mcd_parser.CACHE_DIR = original_cache_dir
