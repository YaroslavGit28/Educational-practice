from django.urls import path

from .views import ChangeOrderStatusView, ManagerOrdersView, WarehouseOrdersView

app_name = "processing"

urlpatterns = [
    path("manager/orders/", ManagerOrdersView.as_view(), name="manager_orders"),
    path("warehouse/orders/", WarehouseOrdersView.as_view(), name="warehouse_orders"),
    path("orders/<int:order_id>/status/", ChangeOrderStatusView.as_view(), name="change_status"),
]
