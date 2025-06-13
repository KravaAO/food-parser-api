import pytest
from unittest.mock import patch
from nutrition_api import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def real_product():
    return {
        "name": "Курячі Стріпси, 6 штук",
        "description": "Смужки білого соковитого курячого філе, що обсмажуються у хрусткій паніровці. Скільки тобі шматочків? Три, щоб з’їсти одному, чи шість для себе і друга або ж дванадцять на велику компанію?",
        "calories": "400 ккал/kcal",
        "fats": "19.3г/g",
        "carbs": "20.2г/g",
        "proteins": "36.3г/g",
        "unsaturated fats": "2.9г/g",
        "sugar": "2.1г/g",
        "salt": "2.7г/g",
        "portion": "160г/g"
    }


@patch("nutrition_api.routes.products.load_all_products")
def test_all_products_route(mock_load_all, client, real_product):
    mock_load_all.return_value = [real_product]
    response = client.get("/all_products/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == real_product["name"]
    assert data[0]["calories"] == real_product["calories"]

@patch("nutrition_api.routes.products.get_product_by_name")
def test_product_by_name_route_found(mock_get, client, real_product):
    mock_get.return_value = real_product
    response = client.get("/products/Курячі%20Стріпси,%206%20штук")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == real_product["name"]
    assert data["description"] == real_product["description"]

@patch("nutrition_api.routes.products.get_product_by_name")
def test_product_by_name_route_not_found(mock_get, client):
    mock_get.return_value = None
    response = client.get("/products/Красті бургер")
    assert response.status_code == 404
    assert "error" in response.get_json()

@patch("nutrition_api.routes.products.get_product_field")
def test_product_field_route_found(mock_get, client):
    mock_get.return_value = "400 ккал/kcal"
    response = client.get("/products/Курячі%20Стріпси,%206%20штук/calories")
    assert response.status_code == 200
    assert response.get_json()["calories"] == "400 ккал/kcal"

@patch("nutrition_api.routes.products.get_product_field")
def test_product_field_route_not_found(mock_get, client):
    mock_get.return_value = None
    response = client.get("/products/Курячі%20Стріпси,%206%20штук/nonexistent")
    assert response.status_code == 404
    assert "error" in response.get_json()
