from flask import request, jsonify
from sqlalchemy import func, desc
from app import app, db, guard
from app.models.Product import Product
from app.models.Product_category import Product_category
from app.models.Address import Address
from app.models.Cart import Cart
from app.models.Cart_items import Cart_items
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
from datetime import datetime, timedelta
from app.schemas import products_schema
from app.schemas import shop_schema
from app.schemas import shops_schema


guard.init_app(app, User)


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


def isCartValid(date):
    diff = datetime.now() - date
    if diff <= timedelta(hours=48):
        return True
    else:
        return False


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
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)
    user = guard.authenticate(email, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    return ret, 200


@app.route("/refresh", methods=["POST"])
def refresh():
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {"access_token": new_token}
    return ret, 200


@app.route("/user-data", methods=["GET", "POST"])
@flask_praetorian.auth_required
def getUserData():
    current_user = flask_praetorian.current_user()
    if request.method == "GET":
        user_orders = Order.query.filter_by(user_id=current_user.id).all()
        user_addresses = Address.query.filter_by(user_id=current_user.id).all()
        user_shops = Shop.query.filter_by(user_id=current_user.id).all()
        user_data = {
            "id": current_user.id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "phone": current_user.phone,
            "picture_dir": current_user.picture_dir,
            "orders": [
                {
                    "id": order.id,
                    "status": order.status,
                    "total": order.total,
                    "created_at": order.created_at,
                }
                for order in user_orders
            ],
            "addresses": [
                {
                    "address_line": address.address_line,
                    "city": address.city,
                    "postal_code": address.postal_code,
                    "country": address.country,
                    "id": address.id,
                }
                for address in user_addresses
            ],
            "shops": [
                {
                    "id": shop.id,
                    "name": shop.name,
                    "city": shop.city,
                    "rating": shop.rating,
                    "items_sold": shop.items_sold,
                    "description": shop.description,
                    "slogan": shop.slogan,
                    "payment_account": shop.payment_account,
                }
                for shop in user_shops
            ],
        }
        try:
            return jsonify(user_data)
        except:
            return "No products found", 404
    if request.method == "POST":
        data = request.get_json()
        if data:
            existing_user = User.query.filter_by(email=data.get("email")).all()
            if existing_user:
                return "User with this email already exists", 409
            current_user.email = data.get("email", current_user.email)
            current_user.first_name = data.get("firstName", current_user.first_name)
            current_user.last_name = data.get("lastName", current_user.last_name)
            current_user.phone = data.get("phone", current_user.phone)
            db.session.commit()
            return "User data updated successfully", 200
        else:
            return "Invalid request data", 400


@app.route("/register", methods=["POST"])
def createUser():
    data = request.get_json()
    if data:
        existing_user = User.query.filter_by(email=data.get("email")).all()
        if existing_user:
            return "User with this email already exists", 409
        new_user = User(
            email=data.get("email"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            phone=data.get("phone"),
            created_at=datetime.now(),
            picture_dir="default_profile.jpg",
            roles="user",
            is_active=True,
        )
        new_user.set_password(data.get("password"))
        db.session.add(new_user)
        db.session.commit()
        return "User data updated successfully", 200
    else:
        return "Invalid request data", 400


@app.route("/address-delete/<int:id>", methods=["POST"])
@flask_praetorian.auth_required
def deleteAddress(id):
    address = Address.query.filter_by(id=id).first()
    if address:
        db.session.delete(address)
        db.session.commit()
        return "Address deleted successfully", 200
    else:
        return "Invalid request data", 400


@app.route("/create-address", methods=["POST"])
@flask_praetorian.auth_required
def createAddress():
    data = request.get_json()
    if data:
        current_user = flask_praetorian.current_user()
        new_Address = Address(
            address_line=data.get("address_line"),
            city=data.get("city"),
            postal_code=data.get("postal_code"),
            country=data.get("country"),
            user_id=current_user.id,
        )
        db.session.add(new_Address)
        db.session.commit()
        address_id = new_Address.id
        return {"id": address_id, "message": "Address created successfully"}, 200
    else:
        return "Invalid request data", 400


@app.route("/create-shop", methods=["POST"])
@flask_praetorian.auth_required
def createShop():
    data = request.get_json()
    if data:
        current_user = flask_praetorian.current_user()
        new_shop = Shop(
            name=data.get("name"),
            city=data.get("city"),
            rating=0,
            items_sold=0,
            description=data.get("description"),
            slogan=data.get("slogan"),
            payment_account=data.get("payment_account"),
            logo_dir="default_shop.png",
            user_id=current_user.id,
        )
        db.session.add(new_shop)
        db.session.commit()
        shop_id = new_shop.id
        return {"id": shop_id, "message": "Shop created successfully"}, 200
    else:
        return "Invalid request data", 400


@app.route("/shop-delete/<int:id>", methods=["DELETE"])
@flask_praetorian.auth_required
def delete_shop(id):
    shop = Shop.query.filter_by(id=id).first()
    if shop:
        db.session.delete(shop)
        db.session.commit()
        return {"message": "Shop deleted successfully"}, 200
    else:
        return {"message": "Shop not found"}, 404


@app.route("/shop-delete/<int:id>", methods=["OPTIONS"])
def delete_shop_preflight(id):
    shop = Shop.query.filter_by(id=id).first()
    if shop:
        return {"message": "Shop exists"}, 200
    else:
        return {"message": "Shop not found"}, 404


@app.route("/cart", methods=["GET"])
@flask_praetorian.auth_required
def getCart():
    current_user = flask_praetorian.current_user()
    carts = (
        Cart.query.filter_by(user_id=current_user.id)
        .order_by(Cart.created_at.desc())
        .all()
    )
    if carts:
        for cart in carts:
            cartValidity = isCartValid(cart.created_at)
            if cartValidity:
                return {"cart_id": cart.id, "message": "Cart exists"}, 200
    else:
        created_at = datetime.strptime(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"
        )
        new_cart = Cart(user_id=current_user.id, created_at=created_at)
        db.session.add(new_cart)
        db.session.commit()
        cart = Cart.query.filter_by(
            user_id=current_user.id, created_at=created_at
        ).first()
        return {"cart_id": cart.id, "message": "Cart created"}, 200


@app.route("/cart-add", methods=["POST"])
@flask_praetorian.auth_required
def add_to_cart():
    current_user = flask_praetorian.current_user()
    carts = (
        Cart.query.filter_by(user_id=current_user.id)
        .order_by(Cart.created_at.desc())
        .all()
    )
    if carts:
        for cart in carts:
            cartValidity = isCartValid(cart.created_at)
            if cartValidity:
                cart_id = cart.id
                break
    else:
        created_at = datetime.strptime(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"
        )
        new_cart = Cart(user_id=current_user.id, created_at=created_at)
        db.session.add(new_cart)
        db.session.commit()
        cart = Cart.query.filter_by(
            user_id=current_user.id, created_at=created_at
        ).first()
        cart_id = cart.id
    data = request.get_json()
    if data:
        new_cart_item = Cart_items(
            cart_id=cart_id,
            product_id=data.get("product_id"),
            quantity=data.get("quantity"),
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return {"message": "Cart item created successfully"}, 200
    else:
        return "Invalid request data", 400
