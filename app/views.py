from flask import request, jsonify
from sqlalchemy import func, desc
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


class ShopSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "city",
            "rating",
            "items_sold",
            "description",
            "slogan",
            "payment_account",
            "logo_dir",
            "user_id",
        )


shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)


@app.route("/products", methods=["GET"])
def getProducts():
    products = Product.query.all()
    return products_schema.jsonify(products)


@app.route("/shop/<int:id>", methods=["GET"])
def getShop(id):
    shop = Shop.query.get(id)
    return shop_schema.jsonify(shop)


@app.route("/shops/best-rated", methods=["GET"])
def getBestRatedShops():
    sorted_shops = Shop.query.order_by(Shop.rating.desc()).all()
    result = sorted_shops[:10]
    return shops_schema.jsonify(result)


@app.route("/products/<string:filter>", methods=["GET"])
def getProductsByFilter(filter):
    if filter == "newest":
        sorted_products = Product.query.order_by(Product.created_at.desc()).all()
        result = sorted_products[:10]
        try:
            return products_schema.jsonify(result)
        except:
            return "No products found", 404
    elif filter == "popular":
        most_sold = (
            db.session.query(
                Order_items.product_id,
                func.sum(Order_items.quantity).label("total_sold"),
            )
            .group_by(Order_items.product_id)
            .order_by(desc("total_sold"))
            .all()[:10]
        )
        result = []
        for item in most_sold:
            product = Product.query.get(item[0])
            result.append(
                {
                    "id": item[0],
                    "name": product.name,
                    "description": product.description,
                    "product_category_id": product.product_category_id,
                    "created_at": product.created_at,
                    "shop_id": product.shop_id,
                    "price": product.price,
                }
            )
        try:
            return jsonify(result)
        except:
            return "No products found", 404
    else:
        result = []
