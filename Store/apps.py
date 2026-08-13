"""
Application configuration for the Store app.
"""

from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
    Configuration class for the Store application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    # This MUST match the Django app folder name.
    name = "Store"