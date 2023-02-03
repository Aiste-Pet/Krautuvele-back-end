import random
from app import db
import requests
import json
import time
import re
import os
import openai
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

openai.api_key = os.environ.get("OPENAI_API_KEY")
base_dir = os.path.abspath(os.path.dirname(__file__))


db.create_all()

# shop = Shop(
#     "Megztukas",
#     "Palanga",
#     4.8,
#     18,
#     "Sveiki, mūsų parduotuvė yra specializuota mezginiais. Galime pasiūlyti plačią pasirinkimą mezgimo drabužių ir aksesuarų, kurie bus patogūs ir patikimi bet kokiam orui. Mes siūlome tik aukštos kokybės produktus, kuriuos gamina mūsų patikimi meistrai. Ateikite ir susipažinkite su mūsų unikaliais mezginiais!",
#     "Mūsų mezginiai - Jūsų šiluma.",
#     "LT123456789",
#     "megztukas.png",
#     1,
# )

# db.session.add_all([shop])
# db.session.commit()

# user = User(
#     "aisvais@gmail.com",
#     "$2b$12$lvvIrO57SwMTmPcqRH71P.Z4obg4kzSPk3qNTMjm9t0xO.IMOzqgy",
#     "Močiutė",
#     "Baba",
#     "+37068514855",
#     datetime.now(),
#     "default_profile.jpg",
# )
# db.session.add_all([user])
# db.session.commit()

# categories = ["Papuošalai", "Apranga", "Aksesuarai", "Interjeras", "Žaislai", "Amatai"]
# for category in categories:
#     categoryItem = Product_category(category)
#     db.session.add(categoryItem)
#     db.session.commit()


# generated_product_names = openai.Completion.create(
#     model="text-babbage-001",
#     prompt="Generate classic product name for a handmade product",
#     temperature=0.9,
#     n=50,
# )


# def seed_products():
#     for item in generated_product_names.choices:
#         product_name = re.sub('"', "", re.sub("\n", " ", item.text).strip())
#         product_price = round(random.uniform(0.01, 99.99), 2)
#         generated_product_description = openai.Completion.create(
#             model="text-babbage-001",
#             prompt=f"Generate {product_name} description",
#             temperature=0,
#             n=1,
#         )
#         product_description = re.sub(
#             "\n", " ", generated_product_description.choices[0].text
#         ).strip()
#         product_category_id = random.randint(1, 6)
#         shop_id = 1
#         product = Product(
#             product_name,
#             product_price,
#             product_description,
#             product_category_id,
#             shop_id,
#         )
#         db.session.add(product)
#         db.session.commit()
#         time.sleep(5)


# seed_products()


def seed_product_images():
    products = Product.query.all()
    for product in products:
        # call API to generate image
        name = product.name
        image_urls = []
        response = openai.Image.create(prompt=name, n=2, size="256x256")
        for item in response["data"]:
            image_urls.append(item["url"])
        for index, url in enumerate(image_urls):
            # Download the image and save it to the assets folder
            response = requests.get(url)
            file_name = f"app/static/product_images/{name[:10]}-{index}.jpg"
            open(
                os.path.join(base_dir, file_name),
                "wb",
            ).write(response.content)
            # Save the image's local directory and product id to the product_image table
            product_image = Product_image(
                product_id=product.id,
                public_dir=file_name,
                type="product image",
            )
            db.session.add(product_image)
            db.session.commit()
        time.sleep(12)


seed_product_images()

# property1 = Product_property("Dydis", "S", 1)
# property2 = Product_property("Dydis", "M", 2)
# property3 = Product_property("Dydis", "L", 3)
# property4 = Product_property("Spalva", "raudona", 4)
# property5 = Product_property("Spalva", "mėlyna", 5)
# property6 = Product_property("Spalva", "žalia", 6)
# property7 = Product_property("Spalva", "geltona", 7)
# property8 = Product_property("Spalva", "balta", 8)
# property9 = Product_property("Spalva", "juoda", 8)
# property10 = Product_property("Ilgis", "trumpas", 9)
# property11 = Product_property("Ilgis", "ilgas", 9)

# db.session.add_all(
#     [
#         property1,
#         property2,
#         property3,
#         property4,
#         property5,
#         property6,
#         property7,
#         property8,
#         property9,
#         property10,
#         property11,
#     ]
# )
# db.session.commit()

# with open("data_seed/products_data.json", "r") as json_file:
#     data = json.load(json_file)
#     for item in data:
#         product = Product(
#             item["name"],
#             item["price"],
#             item["description"],
#             item["product_category_id"],
#             item["shop_id"],
#         )
#         db.session.add(product)
#     db.session.commit()
