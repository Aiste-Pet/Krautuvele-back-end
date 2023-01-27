from flask import request, jsonify
from app import app, db, ma
from app.models.Product import Product


class ProductSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "product_category_id",
            "shop_id",
            "price",
        )


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"about": "Hello World"})


@app.route("/products", methods=["GET"])
def getProducts():
    products = Product.query.all()
    return products_schema.jsonify(products)
