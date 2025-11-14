from django.urls import path
from . import views
from .views import add_to_cart, remove_from_cart, cart_view, product_detail

urlpatterns = [
    path("", views.products, name="products"),
    path("product_detail/<int:product_id>/", product_detail, name="product_detail"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/", cart_view, name="cart"),
]
