from django.urls import path
from . import views

app_name = 'processing'

urlpatterns = [
    path('manager/', views.manager_orders, name='manager_orders'),
    path('manager/confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('manager/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('warehouse/', views.warehouse_orders, name='warehouse_orders'),
    path('warehouse/start/<int:order_id>/', views.start_pickup, name='start_pickup'),
    path('warehouse/complete/<int:order_id>/', views.complete_pickup, name='complete_pickup'),
]