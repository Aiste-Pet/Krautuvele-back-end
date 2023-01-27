from app import db
import json
from datetime import datetime
from app.models.Address import Address
from app.models.Cart import Cart
from app.models.Order_items import Order_items
from app.models.Order import Order
from app.models.Payment import Payment
from app.models.Product_category import Product_category
from app.models.Product_image import Product_image
from app.models.Product_property import Product_property
from app.models.Product import Product
from app.models.Sales import Sales
from app.models.Shop import Shop
from app.models.User import User


db.create_all()

shop = Shop(
    "Megztukas",
    "Palanga",
    4.8,
    18,
    "Sveiki, mūsų parduotuvė yra specializuota mezginiais. Galime pasiūlyti plačią pasirinkimą mezgimo drabužių ir aksesuarų, kurie bus patogūs ir patikimi bet kokiam orui. Mes siūlome tik aukštos kokybės produktus, kuriuos gamina mūsų patikimi meistrai. Ateikite ir susipažinkite su mūsų unikaliais mezginiais!",
    "Mūsų mezginiai - Jūsų šiluma.",
    "LT123456789",
    "megztukas.png",
    1,
)

db.session.add_all([shop])
db.session.commit()

user = User(
    "aisvais@gmail.com",
    "$2b$12$lvvIrO57SwMTmPcqRH71P.Z4obg4kzSPk3qNTMjm9t0xO.IMOzqgy",
    "Močiutė",
    "Baba",
    "+37068514855",
    datetime.now(),
    "default_profile.jpg",
)
db.session.add_all([user])
db.session.commit()

category1 = Product_category("Dydis")
category2 = Product_category("Spalva")
category3 = Product_category("Ilgis")

db.session.add_all([category1, category2, category3])
db.session.commit()

with open("data_seed/products_data.json", "r") as json_file:
    data = json.load(json_file)
    for item in data:
        product = Product(
            item["name"],
            item["price"],
            item["description"],
            item["product_category_id"],
            item["shop_id"],
        )
        db.session.add(product)
    db.session.commit()
