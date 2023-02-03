from flask import request, jsonify
from app import app, db, ma
from app.models.Product import Product
from app.models.Product_category import Product_category


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


@app.route("/products", methods=["GET"])
def getProducts():
    products = Product.query.all()
    return products_schema.jsonify(products)


@app.route("/categories", methods=["GET"])
def getCategories():
    categories = Product_category.query.all()
    return products_schema.jsonify(categories)
