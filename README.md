<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue" />
  <img src="https://img.shields.io/badge/Flask-2.3-lightgrey" />
  <img src="https://img.shields.io/badge/Selenium-headless-green" />
  <img src="https://img.shields.io/badge/Docker-supported-blue" />
</p>

## API Endpoints

### `GET /all_products/`

Returns all available product data in JSON format.

#### ✅ Success Response:

```json
[
  {
    "name": "Тейсті Джуніор",
    "description": "Класика, яку обожнюєш...",
    ...
  },
  ...
]
```

#### Error Response:

```json
{
  "error": "Could not read the products file"
}
```

---

### `GET /products/<product_name>`

Returns full information for a specific product.

#### Success Response:

```json
{
  "name": "Чікен Рол",
  "description": "Загорнуті в тонкий...",
  ...
}
```

#### Not Found:

```json
{
  "error": "Product not found"
}
```

#### Internal Server Error:

```json
{
  "error": "Parsing failed or product unavailable"
}
```

---

### `GET /products/<product_name>/<field>`

Returns only the requested field (e.g., calories, fats) for a specific product.

#### Success Response:

```json
{
    "name": "МакКріспі Делюкс"
}
```

#### Bad Request:

```json
{
  "error": "Field 'some_field' is not allowed"
}
```

#### Not Found:

```json
{
  "error": "Product not found"
}
```

#### Internal Server Error:

```json
{
  "error": "Parsing failed or product unavailable"
}
```

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
