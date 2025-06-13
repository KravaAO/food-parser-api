from flask import Flask

def create_app():
    app = Flask(__name__)

    from nutrition_api.routes.products import products_bp
    app.register_blueprint(products_bp, url_prefix="/")

    return app
