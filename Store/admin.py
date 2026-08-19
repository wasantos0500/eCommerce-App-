"""
Admin configuration for the Store application.

This file registers the application's models so that they can
be viewed and managed through Django's built-in administration site.
"""

from django.contrib import admin
from .models import Store, Product, Review, Order, OrderItem


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Admin configuration for Store objects.
    """
    
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__username")
    list_filter = ("created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for Review objects.
    """

    list_display = ("product", "reviewer", "rating", "verified")
    list_filter = ("verified", "rating")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order objects.
    """

    list_display = ("id", "buyer", "created_at", "total_price")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrderItem objects.
    """

    list_display = ("order", "product", "quantity", "price")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "store",
        "price",
        "stock",
        "available",
    )

    search_fields = (
        "name",
        "store__name",
    )

    list_filter = (
        "available",
        "store",
    )