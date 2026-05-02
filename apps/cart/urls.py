from django.urls import path

from .views import AddToCartView, CartView, ClearCartView, RemoveCartItemView, UpdateCartItemView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="view"),
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add"),
    path("update/<int:item_id>/", UpdateCartItemView.as_view(), name="update"),
    path("remove/<int:item_id>/", RemoveCartItemView.as_view(), name="remove"),
    path("clear/", ClearCartView.as_view(), name="clear"),
]
