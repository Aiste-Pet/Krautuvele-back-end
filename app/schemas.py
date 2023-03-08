from app import ma


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


class OrderSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "total",
            "created_at",
            "status",
        )


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


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
            "logo_dir",
            "user_id",
        )


shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)
