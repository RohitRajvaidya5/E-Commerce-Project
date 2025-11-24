from django.urls import path
from . import views
from .views import (
    add_to_cart,
    remove_from_cart,
    cart_view,
    product_detail,
    search_products,
    search_suggestions,
    update_cart_quantity,
    checkout,
    test_email,
)
from .views import run_migrations


urlpatterns = [
    path("", views.products, name="products"),
    path("product_detail/<int:product_id>/", product_detail, name="product_detail"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/", cart_view, name="cart"),
    path(
        "update-cart-quantity/<int:product_id>/<int:quantity>/",
        update_cart_quantity,
        name="update_cart_quantity",
    ),
    path("search/", search_products, name="search"),
    path("search-suggestions/", search_suggestions, name="search_suggestions"),
    path("checkout/", checkout, name="checkout"),
    path("success/", views.success, name="success"),
    path("test-email/", test_email, name="test_email"),
    path("run-migrations/", run_migrations),
]
