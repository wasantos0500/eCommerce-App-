"""
Forms used throughout the Store application.

This module contains forms related to user authentication and
registration.
"""

from django import forms
from django.contrib.auth.models import User
from .models import Store, Product, Review


class RegisterForm(forms.ModelForm):
    """
    Form used to register a new user.

    Users can choose whether they want to register as a Buyer
    or a Vendor. The selected role will later be assigned
    using Django Groups.
    """

    ROLE_CHOICES = [
        ("Buyer", "Buyer"),
        ("Vendor", "Vendor"),
    ]

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "role",
        ]

    def clean(self):
        """
        Ensure both passwords entered by the user match.
        """

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

class StoreForm(forms.ModelForm):
    """
    Form used to create and update Store instances.
    """

    class Meta:
        model = Store

        fields = [
            "name",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Store name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your store...",
                }
            ),
        }

class ProductForm(forms.ModelForm):
    """
    Form used to create and edit products.
    """

    class Meta:
        model = Product

        fields = [
            "store",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "available",
        ]

    def __init__(self, *args, **kwargs):
        """
        Limit available stores to those owned by the logged-in vendor.
        """

        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user:
            self.fields["store"].queryset = Store.objects.filter(
                owner=user
            )

class ReviewForm(forms.ModelForm):
    """
    Form used by buyers to leave a product review.
    """

    class Meta:
        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {
            "rating": forms.Select(
                attrs={
                    "class": "form-select",
                },
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }