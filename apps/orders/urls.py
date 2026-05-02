from django.urls import path

from .views import CancelOrderView, CheckoutView, MyOrdersView, OrderDetailView

app_name = "orders"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("my/", MyOrdersView.as_view(), name="my_orders"),
    path("cancel/<int:order_id>/", CancelOrderView.as_view(), name="cancel"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
]
