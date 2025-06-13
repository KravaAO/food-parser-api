<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue" />
  <img src="https://img.shields.io/badge/Flask-2.3-lightgrey" />
  <img src="https://img.shields.io/badge/Selenium-headless-green" />
  <img src="https://img.shields.io/badge/Docker-supported-blue" />
</p>

## API Endpoints

GET /all_products/
    → Returns all available product data in JSON format.

GET /products/<product_name>
    → Returns full information for a specific product.

GET /products/<product_name>/<field>
    → Returns only the requested field (e.g., calories, fats) for a specific product.

## Running Locally

```bash
git clone https://github.com/KravaAO/food-parser-api.git
cd food-parser-api
git checkout dev
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m nutrition_api

```

## Docker Support
```bash
docker build -t food-api .
docker run -p 8000:8000 food-api
```
After launching, the API will be available at http://localhost:8000
