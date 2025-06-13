from flask import Blueprint, jsonify
from nutrition_api.services.product_service import (
    load_all_products,
    get_product_by_name,
    get_product_field
)

products_bp = Blueprint("products", __name__)

@products_bp.route("/all_products/", methods=["GET"])
def all_products():
    return jsonify(load_all_products())

@products_bp.route("/products/<string:product_name>", methods=["GET"])
def product_by_name(product_name):
    product = get_product_by_name(product_name)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@products_bp.route("/products/<string:product_name>/<string:field>", methods=["GET"])
def product_field(product_name, field):
    value = get_product_field(product_name, field)
    if value is not None:
        return jsonify({field: value})
    return jsonify({"error": "Field not found or product not found"}), 404
