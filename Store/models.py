from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    """
    Represents an online store owned by a vendor.

    A single authenticated user can own one or more stores.
    Buyers can browse stores and purchase their products.
    """

    # The vendor who owns the store.
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stores"
    )

    # Store name displayed throughout the application.
    name = models.CharField(max_length=100)

    # Optional description about the store.
    description = models.TextField(blank=True)

    # Date when the store was created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the store name when displayed in Django Admin."""
        return self.name


class Product(models.Model):
    """
    Represents a product sold within a vendor's store.
    """

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )

    available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        Return the product name.
        """

        return self.name

    @property
    def in_stock(self):
        """
        Check if the product is in stock.
        """

        return self.stock > 0


from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Represents a review left by a buyer for a product.

    A review can later be marked as verified if the buyer
    purchased the product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    RATING_CHOICES = [
        (5, "★★★★★ - Excellent"),
        (4, "★★★★☆ - Very Good"),
        (3, "★★★☆☆ - Good"),
        (2, "★★☆☆☆ - Fair"),
        (1, "★☆☆☆☆ - Poor"),
    ]

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(5),
        ],
    )

    comment = models.TextField()

    # Indicates whether the reviewer purchased the product.
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.rating}/5)"

    @property
    def stars(self):
        """
        Return a string representation of the rating in stars.
        """

        return "★" * self.rating + "☆" * (5 - self.rating)

class Order(models.Model):
    """
    Represents a buyer's completed purchase.
    """

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def item_count(self):
        return self.items.count()

    @property
    def total_quantity(self):
        """
        Calculate the total quantity of items in the order.
        """
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    """
    Represents an individual product within an order.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        """
        Calculate the subtotal for this order item.
        """
        return self.price * self.quantity