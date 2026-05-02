from rest_framework import serializers

from apps.cart.models import CartItem
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "phone", "address", "role")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "total_price")


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product_name", "quantity", "price_at_moment", "subtotal")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_name = serializers.CharField(source="status.name", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status_name",
            "total_amount",
            "delivery_address",
            "phone",
            "comment",
            "created_at",
            "items",
        )
