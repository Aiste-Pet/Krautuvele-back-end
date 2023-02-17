from flask import request, jsonify
from sqlalchemy import func, desc
from app import app, db, ma, guard
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
import flask_praetorian
from flask import jsonify

guard.init_app(app, User)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "picture_dir",
        )


user_schema = UserSchema()


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


def gatherProductData(result, product):
    query_product_images = Product_image.query.filter_by(product_id=product.id).all()
    shop = Shop.query.filter_by(id=product.shop_id).first()
    category = Product_category.query.filter_by(id=product.product_category_id).first()
    product_images = []
    for image in query_product_images:
        product_images.append(image.public_dir)
    if result == {}:
        result = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "product_category_name": category.name,
            "created_at": product.created_at,
            "shop_id": product.shop_id,
            "shop_name": shop.name,
            "price": product.price,
            "product_images": product_images,
        }
    else:
        result.append(
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "product_category_name": category.name,
                "created_at": product.created_at,
                "shop_id": product.shop_id,
                "price": product.price,
                "product_images": product_images,
            }
        )
    return result


def filterByCategory(category_name):
    category = Product_category.query.filter_by(name=category_name).first()
    if not category:
        return "Category not found", 404
    products = Product.query.filter_by(product_category_id=category.id).all()
    result = []
    for product in products:
        result = gatherProductData(result, product)
    try:
        return jsonify(result)
    except:
        return "No products found", 404


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


@app.route("/product/<int:id>", methods=["GET"])
def getProduct(id):
    product = Product.query.get(id)
    result = {}
    result = gatherProductData(result, product)
    try:
        return jsonify(result)
    except:
        return "No products found", 404


@app.route("/shop/<int:id>", methods=["GET"])
def getShop(id):
    shop = Shop.query.get(id)
    return shop_schema.jsonify(shop)


@app.route("/shop-products/<int:id>", methods=["GET"])
def getShopProducts(id):
    products = Product.query.filter_by(shop_id=id).all()
    result = []
    for product in products:
        result = gatherProductData(result, product)
    try:
        return jsonify(result)
    except:
        return "No products found", 404


@app.route("/shops/best-rated", methods=["GET"])
def getBestRatedShops():
    sorted_shops = Shop.query.order_by(Shop.rating.desc()).all()
    result = sorted_shops[:10]
    return shops_schema.jsonify(result)


@app.route("/products/category/<string:filter>", methods=["GET"])
def getProductsByFilter(filter):
    if filter == "Naujienos":
        products = Product.query.order_by(Product.created_at.desc()).all()
        result = []
        for product in products:
            result = gatherProductData(result, product)
        try:
            return jsonify(result)
        except:
            return "No products found", 404
    elif filter == "Populiaru":
        most_sold_products = (
            db.session.query(
                Order_items.product_id,
                func.sum(Order_items.quantity).label("total_sold"),
            )
            .group_by(Order_items.product_id)
            .order_by(desc("total_sold"))
            .all()
        )
        result = []
        for item in most_sold_products:
            product = Product.query.get(item[0])
            result = gatherProductData(result, product)
        try:
            return jsonify(result)
        except:
            return "No products found", 404
    else:
        result = filterByCategory(filter)
        return result


@app.route("/categories", methods=["GET"])
def getCategories():
    categories = Product_category.query.all()
    return products_schema.jsonify(categories)


@app.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    """
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)
    user = guard.authenticate(email, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    return ret, 200


@app.route("/refresh", methods=["POST"])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    """
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {"access_token": new_token}
    return ret, 200


@app.route("/protected")
@flask_praetorian.auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    """
    return {
        "message": f"protected endpoint (allowed user {guard.current_user().email})"
    }


@app.route("/user-data", methods=["GET"])
@flask_praetorian.auth_required
def getUserData():
    """
    Returns user data for a user with a valid JWT token.
    """
    current_user = flask_praetorian.current_user()
    result = {}
    result = {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone": current_user.phone,
        "picture_dir": current_user.picture_dir,
    }
    try:
        return jsonify(result)
    except:
        return "No products found", 404
