from django.urls import path

from . import api_views


urlpatterns = [
    # Basic API test endpoint.
    path(
        "",
        api_views.api_home,
        name="api_home",
    ),

    # Store API endpoints.
    path(
        "stores/",
        api_views.store_list_api,
        name="api_store_list",
    ),

    path(
        "stores/<int:pk>/",
        api_views.store_detail_api,
        name="api_store_detail",
    ),

    path(
        "stores/<int:pk>/products/",
        api_views.store_products_api,
        name="api_store_products",
    ),

    # Product API endpoints.
    path(
        "products/",
        api_views.product_list_api,
        name="api_product_list",
    ),

    path(
        "products/<int:pk>/",
        api_views.product_detail_api,
        name="api_product_detail",
    ),

    # Review API endpoints.
    path(
        "reviews/",
        api_views.review_list_api,
        name="api_review_list",
    ),

    path(
        "products/<int:pk>/reviews/",
        api_views.product_reviews_api,
        name="api_product_reviews",
    ),
]