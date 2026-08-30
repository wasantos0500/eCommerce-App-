"""
Main URL configuration for the eCommerce application.
"""

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Django administration site
    path("admin/", admin.site.urls),

    # Store application
    path("", include("store.urls")),

    # Authentication views
    path(
        "authentication/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/password_reset.html"
        ),
        name="password_reset",
    ),

    path(
        "authentication/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "authentication/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    path(
        "authentication/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # REST API endpoints
    path("api/", include("store.api_urls")),

    # Django REST Framework's built-in authentication views
    path("api-auth/", include("rest_framework.urls")),
]
