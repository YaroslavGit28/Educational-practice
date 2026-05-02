from django.db import transaction
from django.db.models import Sum
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.cart.models import CartItem
from apps.cart.services import get_cart_queryset, get_session_key
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem, OrderStatus

from .serializers import CartItemSerializer, CategorySerializer, OrderSerializer, ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartApiView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(CartItemSerializer(get_cart_queryset(request), many=True).data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def cart_add(request):
    product = Product.objects.get(pk=request.data.get("product_id"))
    quantity = int(request.data.get("quantity", 1))
    key = get_session_key(request)
    if request.user.is_authenticated:
        item, _ = CartItem.objects.get_or_create(user=request.user, product=product, defaults={"quantity": quantity})
    else:
        item, _ = CartItem.objects.get_or_create(session_key=key, user=None, product=product, defaults={"quantity": quantity})
    item.quantity = quantity
    item.save()
    return Response({"ok": True})


@api_view(["POST"])
def cart_update(request):
    item = CartItem.objects.get(pk=request.data.get("item_id"), user=request.user)
    item.quantity = int(request.data.get("quantity", 1))
    item.save(update_fields=["quantity"])
    return Response({"ok": True})


@api_view(["DELETE"])
@permission_classes([permissions.AllowAny])
def cart_remove(request, item_id):
    get_cart_queryset(request).filter(pk=item_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class OrdersApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(OrderSerializer(Order.objects.filter(user=request.user), many=True).data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def checkout_api(request):
    cart_items = get_cart_queryset(request)
    if not cart_items.exists():
        return Response({"detail": "empty cart"}, status=400)
    with transaction.atomic():
        status_obj = OrderStatus.objects.get_or_create(name="new", defaults={"description": "Новый"})[0]
        order = Order.objects.create(
            user=request.user,
            full_name=request.user.full_name,
            status=status_obj,
            delivery_address=request.data.get("delivery_address", request.user.address),
            phone=request.data.get("phone", request.user.phone),
            comment=request.data.get("comment", ""),
        )
        total = 0
        for item in cart_items:
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity, price_at_moment=item.product.price
            )
            item.product.stock = max(0, item.product.stock - item.quantity)
            item.product.save(update_fields=["stock"])
            total += item.product.price * item.quantity
        order.total_amount = total
        order.save(update_fields=["total_amount"])
        cart_items.delete()
    return Response(OrderSerializer(order).data, status=201)


class ManagerOrdersApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ["manager", "admin"]:
            return Response({"detail": "forbidden"}, status=403)
        data = OrderSerializer(Order.objects.all(), many=True).data
        return Response(data)

    def patch(self, request, order_id):
        if request.user.role not in ["manager", "admin"]:
            return Response({"detail": "forbidden"}, status=403)
        order = Order.objects.get(pk=order_id)
        order.status = OrderStatus.objects.get(name=request.data.get("status"))
        order.save(update_fields=["status"])
        return Response({"ok": True})


class WarehouseOrdersApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ["warehouse", "admin"]:
            return Response({"detail": "forbidden"}, status=403)
        return Response(OrderSerializer(Order.objects.filter(status__name="confirmed"), many=True).data)


class SalesReportApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"detail": "forbidden"}, status=403)
        rows = (
            Order.objects.values("created_at__date")
            .annotate(amount=Sum("total_amount"))
            .order_by("-created_at__date")[:30]
        )
        return Response(list(rows))
