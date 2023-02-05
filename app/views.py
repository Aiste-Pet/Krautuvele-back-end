from flask import request, jsonify
from app import app, db, ma
from app.models.Product import Product
from app.models.Product_category import Product_category
from app.models.Address import Address
from app.models.Cart import Cart
from app.models.Order_items import Order_items
from app.models.Order import Order
from app.models.Payment import Payment
from app.models.Product_image import Product_image
from app.models.Product_property import Product_property
from app.models.Sales import Sales
from app.models.Shop import Shop
from app.models.User import User


class ProductSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "product_category_id",
            "created_at",
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
