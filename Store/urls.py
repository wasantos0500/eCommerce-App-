"""
URL configuration for the Store application.

Each URL maps a browser request to the appropriate view.
"""

from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    # Home page
    path("", views.home, name="home"),

    # User authentication
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard and store management
    path("dashboard/", views.dashboard, name="dashboard"),

    # Product management
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.create_product, name="create_product"),

    # Shopping cart
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    # Store CRUD
    path("stores/create/", views.create_store, name="create_store"),
    path("stores/<int:pk>/", views.store_detail, name="store_detail"),
    path("stores/<int:pk>/edit/", views.update_store, name="update_store"),
    path("stores/<int:pk>/delete/", views.delete_store, name="delete_store"),

    # Product CRUD
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/edit/", views.update_product, name="update_product"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"), 

    # Public-facing views
    path("stores/", views.browse_stores, name="browse_stores"),
    path("stores/<int:pk>/products/", views.public_store_detail, name="public_store_detail"),
    path("browse/", views.browse_products, name="browse_products"),
    path("products/<int:pk>/view/", views.public_product_detail, name="public_product_detail"),

    # Shopping cart management
    path("cart/remove/<int:product_id>/",views.remove_from_cart,name="remove_from_cart"),
    path("cart/increase/<int:product_id>/",views.increase_quantity,name="increase_quantity"),
    path("cart/decrease/<int:product_id>/",views.decrease_quantity,name="decrease_quantity"),
    path("cart/clear/",views.clear_cart,name="clear_cart"),

    # checkout and order management
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/", views.order_confirmation, name="order_confirmation"),

    # Review management
    path("products/<int:product_id>/review/", views.add_review, name="add_review"),

    # External/Reddit API integration
    path("reddit/", views.reddit_feed, name="reddit_feed"),
]


