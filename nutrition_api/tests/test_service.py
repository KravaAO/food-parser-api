import pytest
from unittest.mock import patch
from nutrition_api.services import product_service


@pytest.fixture
def sample_product():
    return {
        "name": "Test Burger",
        "description": "A tasty test burger",
        "calories": "300",
        "fats": "15",
        "carbs": "20",
        "proteins": "10",
        "unsaturated fats": "5",
        "sugar": "2",
        "salt": "1",
        "portion": "150г"
    }


@patch("nutrition_api.services.product_service.get_product_ids")
@patch("nutrition_api.services.product_service.fetch_product_data")
@patch("nutrition_api.services.product_service.webdriver.Chrome")
def test_get_product_by_name(mock_driver, mock_fetch_data, mock_get_ids, sample_product):
    mock_driver.return_value.quit = lambda: None
    mock_get_ids.return_value = (["1"], [{"id": "1", "name": sample_product["name"]}])
    mock_fetch_data.return_value = sample_product

    result = product_service.get_product_by_name(sample_product["name"])
    assert result["name"] == sample_product["name"]


@patch("nutrition_api.services.product_service.get_product_by_name")
def test_get_product_field(mock_get_by_name, sample_product):
    mock_get_by_name.return_value = sample_product

    result = product_service.get_product_field("Test Burger", "calories")
    assert result == sample_product["calories"]

    result_none = product_service.get_product_field("Test Burger", "nonexistent")
    assert result_none is None
