"""
Utility functions used throughout the Store application.

These helper functions reduce duplicated code and improve readability.
"""

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Store, Product


def get_vendor_store(request, pk):
    """
    Retrieve a store that belongs to the currently logged-in vendor.

    Returns:
        Store instance if the store belongs to the vendor.

    Raises:
        PermissionDenied:
            If the authenticated user is not the owner of the store.
    """

    return get_object_or_404(
        Store,
        pk=pk,
        owner=request.user
    )   


def get_vendor_product(request, pk):
    """
    Retrieve a product that belongs to one of the
    logged-in vendor's stores.

    Returns:
        Product instance if the product belongs to the vendor.
    
    Raises:
        Http404: If the product does not exist or does not
        belong to the vendor.

    """

    return get_object_or_404(
        Product,
        pk=pk,
        store__owner=request.user
    )