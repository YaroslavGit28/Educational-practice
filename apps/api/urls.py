from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    CartApiView,
    ManagerOrdersApiView,
    OrdersApiView,
    ProductViewSet,
    CategoryViewSet,
    SalesReportApiView,
    WarehouseOrdersApiView,
    checkout_api,
    cart_add,
    cart_remove,
    cart_update,
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="api-products")
router.register("categories", CategoryViewSet, basename="api-categories")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", obtain_auth_token, name="api-token"),
    path("cart/", CartApiView.as_view(), name="api-cart"),
    path("cart/add/", cart_add, name="api-cart-add"),
    path("cart/update/", cart_update, name="api-cart-update"),
    path("cart/remove/<int:item_id>/", cart_remove, name="api-cart-remove"),
    path("checkout/", checkout_api, name="api-checkout"),
    path("orders/", OrdersApiView.as_view(), name="api-orders"),
    path("manager/orders/", ManagerOrdersApiView.as_view(), name="api-manager-orders"),
    path("manager/order/<int:order_id>/", ManagerOrdersApiView.as_view(), name="api-manager-order-update"),
    path("warehouse/orders/", WarehouseOrdersApiView.as_view(), name="api-warehouse-orders"),
    path("reports/sales/", SalesReportApiView.as_view(), name="api-reports-sales"),
]
