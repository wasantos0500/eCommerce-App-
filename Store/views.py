"""
Views for the Store application.

This module contains the core views used for the home page,
user registration and authentication.
"""

# Standard library imports
from decimal import Decimal
from .functions.reddit import get_reddit_posts

# Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

# Local imports
from .decorators import buyer_required, vendor_required
from .forms import StoreForm, ProductForm, ReviewForm, RegisterForm
from .models import Store, Product, Order, OrderItem, Review
from .utils import get_vendor_store, get_vendor_product


from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

def home(request):
    """
    Display the application's home page.
    """

    return render(request, "home.html")


def register(request):
    """
    Register a new user.

    The selected role (Buyer or Vendor) determines which
    Django Group the new user is added to.
    """

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # Hash the password before saving the user.
            user.set_password(form.cleaned_data["password"])

            user.save()

            role = form.cleaned_data["role"]

            group = Group.objects.get(name=role)

            user.groups.add(group)

            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully!"
            )

        # Send a welcome email to the new user.
            send_mail(
                subject="Welcome to Our E-commerce Platform!",
                message=(
                    f"Hi {user.first_name},\n\n"
                    "Thank you for registering as a {role}!"
                    "\n\nBest regards,\nThe E-commerce Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


def login_view(request):
    """
    Authenticate an existing user.
    """

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("home")

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


def logout_view(request):
    """
    Log the current user out.
    """

    logout(request)

    messages.info(
        request,
        "You have been logged out."
    )

    return redirect("home")

@login_required
@vendor_required
def dashboard(request):
    """
    Display the vendor dashboard.

    Vendors can see all stores that they own.
    """

    stores = Store.objects.filter(owner=request.user)

    context = {
        "stores": stores,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )


@login_required
@vendor_required
def create_store(request):
    """
    Create a new store owned by the current vendor.
    """

    form = StoreForm(
        request.POST or None
    )

    if form.is_valid():

        store = form.save(commit=False)

        store.owner = request.user

        store.save()

        messages.success(
            request,
            "Your store has been created successfully."
        )

        return redirect("dashboard")

    return render(
        request,
        "stores/store_form.html",
        {
            "form": form,
            "title": "Create Store",
        },
    )

@login_required
@vendor_required
def product_list(request):
    """
    Display all products that belong to the current vendor.
    """

    products = Product.objects.filter(
        store__owner=request.user
    ).select_related("store")

    return render(
        request,
        "products/product_list.html",
        {
            "products": products
        }
    )


@login_required
@vendor_required
def create_product(request):
    """
    Allow a vendor to add a product to one of their stores.
    """

    stores = Store.objects.filter(owner=request.user)

    if not stores.exists():

        messages.warning(
            request,
            "Please create a store before adding products."
        )

        return redirect("dashboard")

    if request.method == "POST":

        form = ProductForm(
            request.POST or None,
            request.FILES or None,
            user=request.user
        )

        if form.is_valid():

            product = form.save(commit=False)
            product.save()

            messages.success(
                request,
                "Product created successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm(user=request.user)

    return render(
        request,
        "create_product.html",
        {
            "form": form
        }
    )

"""
____________________________________________
The following views are for the shopping cart 
functionality. 
____________________________________________
"""
@login_required
@buyer_required
def cart(request):
    """
    Display the shopping cart stored in the user's session.
    """

    cart = request.session.get("cart", {})

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    items = []

    total = 0

    for product in products:

        quantity = cart[str(product.id)]

        subtotal = quantity * product.price

        total += subtotal

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total,
        },
    )

@login_required
@buyer_required
def add_to_cart(request, product_id):
    """
    Add a product to the shopping cart.
    """

    cart = request.session.get("cart", {})

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    product_id = str(product.id)

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session["cart"] = cart

    messages.success(
        request,
        "Product added to cart."
    )

    return redirect("cart")

def browse_products(request):
    """
    Display all products available in the store.
    """

    products = Product.objects.filter(
        available=True
    ).select_related("store")

    return render(
        request,
        "buyer/product_list.html",
        {
            "products": products
        }
    )

"""
The following views are for vendor-specific functionality,
such as managing stores and products.
"""

@login_required
@vendor_required
def dashboard(request):
    """
    Display all stores owned by the logged-in vendor.
    """

    stores = Store.objects.filter(owner=request.user)

    context = {
        "stores": stores,
    }

    return render(
        request,
        "stores/store_list.html",
        context,
    )

@login_required
@vendor_required
def store_detail(request, pk):
    """
    Display the details of a single store.

    Only the owner of the store may access this page.
    """

    store = get_vendor_store(request, pk)

    return render(
        request,
        "stores/store_detail.html",
        {
            "store": store,
        },
    )

@login_required
@vendor_required
def update_store(request, pk):
    """
    Update an existing store.

    Vendors can only edit their own stores.
    """

    store = get_vendor_store(request, pk)

    form = StoreForm(
        request.POST or None,
        instance=store,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Store updated successfully."
        )

        return redirect(
            "store_detail",
            pk=store.pk,
        )

    return render(
        request,
        "stores/store_form.html",
        {
            "form": form,
            "title": "Edit Store",
        },
    )

@login_required
@vendor_required
def delete_store(request, pk):
    """
    Delete one of the vendor's stores.
    """

    store = get_vendor_store(request, pk)

    if request.method == "POST":

        store.delete()

        messages.success(
            request,
            "Store deleted successfully."
        )

        return redirect("dashboard")

    return render(
        request,
        "stores/store_confirm_delete.html",
        {
            "store": store,
        },
    )

@login_required
@vendor_required
def product_detail(request, pk):    
    """
    Display the details of a single product.

    Only the owner of the product's store may access this page.
    """

    product = get_vendor_product(request, pk)

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
        },
    )

@login_required
@vendor_required
def update_product(request, pk):
    """
    Update an existing product.

    Vendors can only edit products that belong to their own stores.
    """

    product = get_vendor_product(request, pk)

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product,
        user=request.user
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Product updated successfully."
        )

        return redirect(
            "product_detail",
            pk=product.pk,
        )

    return render(
        request,
        "products/product_form.html",
        {
            "form": form,
            "title": "Edit Product",
        },
    )

@login_required
@vendor_required
def delete_product(request, pk):
    """
    Delete a product that belongs to one of the vendor's stores.
    """

    product = get_vendor_product(request, pk)

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "products/product_confirm_delete.html",
        {
            "product": product,
        },
    )


def browse_stores(request):
    """
    Display all stores available to customers.
    """

    stores = Store.objects.prefetch_related("products").all()

    return render(
        request,
        "buyer/store_list.html",
        {
            "stores": stores,
        },
    )

def public_store_detail(request, pk):
    """
    Display a store and all of its available products.
    """

    store = get_object_or_404(Store, pk=pk)

    products = store.products.filter(
        available=True
    ).order_by("name")

    return render(
        request,
        "buyer/store_detail.html",
        {
            "store": store,
            "products": products,
        },
    )

from .models import Review
def public_product_detail(request, pk):
    """
    Display the details of a product to the public.

    This view is accessible to all users, including 
    unauthenticated visitors.
    """

    product = get_object_or_404(
        Product, 
        pk=pk,
        available=True,
    )

    reviews = product.reviews.all()

    existing_review = None

    if request.user.is_authenticated:
    
            existing_review = Review.objects.filter(
                reviewer=request.user,
                product=product,
            ).first()

    return render(
        request,
        "buyer/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "existing_review": existing_review,
        },
    )
@login_required
@buyer_required
def remove_from_cart(request, product_id):
    """
    Remove a product from the shopping cart.
    """

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

    request.session["cart"] = cart

    messages.success(
        request,
        "Product removed from cart."
    )

    return redirect("cart")

@login_required
@buyer_required
def increase_quantity(request, product_id):
    """
    Increase the quantity of a product in the shopping cart.
    """

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] += 1

    request.session["cart"] = cart

    messages.success(
        request,
        "Product quantity increased."
    )

    return redirect("cart")

@login_required
@buyer_required
def decrease_quantity(request, product_id):
    """
    Decrease the quantity of a product in the shopping cart.
    If the quantity reaches zero, the product is removed from the cart.
    """

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        if cart[product_id] > 1:

            cart[product_id] -= 1

        else:

            del cart[product_id]

    request.session["cart"] = cart

    messages.success(
        request,
        "Product quantity decreased."
    )

    return redirect("cart")

@login_required
@buyer_required
def clear_cart(request):
    """
    Empty the shopping cart.
    """

    request.session["cart"] = {}

    messages.success(
        request,
        "Shopping cart emptied."
    )

    return redirect("cart")

from .models import Order, OrderItem

@login_required
@buyer_required
@transaction.atomic
def checkout(request):
    """
    Complete the checkout process.

    This view:
    - Creates an Order.
    - Creates OrderItem records.
    - Updates stock.
    - Calculates the order total.
    - Clears the shopping cart.
    """

    cart = request.session.get("cart", {})

    if not cart:

        messages.warning(
            request,
            "Your shopping cart is empty."
        )

        return redirect("cart")

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    # Create the order with an initial total.
    order = Order.objects.create(
        buyer=request.user,
        total_price=Decimal("0.00"),
    )

    total = Decimal("0.00")

    for product in products:

        quantity = cart[str(product.id)]

        # Prevent purchasing more than available stock.
        if quantity > product.stock:

            messages.error(
                request,
                f"Not enough stock for '{product.name}'."
            )

            return redirect("cart")

        line_total = product.price * quantity

        total += line_total

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,

            # Store the product price at the
            # time of purchase.
            price=product.price,
        )

        # Reduce stock.
        product.stock -= quantity
        product.save()

    # Save the final order total.
    order.total_price = total
    order.save()

    # Build a simple order summary.
    lines = []

    for item in order.items.all():

        lines.append(
            f"{item.product.name} x {item.quantity} "
            f"- £{item.subtotal}"
        )

    email_message = (
        f"Hello {request.user.username},\n\n"
        "Thank you for your order!\n\n"
        f"Order Number: #{order.id}\n\n"
        "Items:\n"
        + "\n".join(lines)
        + f"\n\nTotal: £{order.total_price}\n\n"
        "We appreciate your purchase."
    )

    send_mail(
        subject=f"Order Confirmation #{order.id}",
        message=email_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=True,
    )

    # Empty the shopping cart.
    request.session["cart"] = {}

    messages.success(
        request,
        "Your order has been placed successfully!"
    )

    return redirect(
        "order_confirmation",
        order_id=order.id,
    )

@login_required
@buyer_required
def order_confirmation(request, order_id):
    """
    Display the order confirmation page after a successful checkout.
    """

    order = get_object_or_404(Order, id=order_id, buyer=request.user)

    items = order.items.select_related("product").all()

    return render(
        request,
        "orders/order_confirmation.html",
        {
            "order": order,
            "items": items,
        }
    )

@login_required
@buyer_required
def add_review(request, product_id):
    """
    Allow a buyer to review a product.

    Buyers may only leave one review per product.
    """

    product = get_object_or_404(
        Product,
        pk=product_id,
    )

    # Prevent duplicate reviews.
    if Review.objects.filter(
        reviewer=request.user,
        product=product,
    ).exists():

        messages.warning(
            request,
            "You have already reviewed this product."
        )

        return redirect(
            "public_product_detail",
            pk=product.id,
        )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.product = product

            review.reviewer = request.user

            # Determine whether the buyer
            # has purchased this product.
            review.verified = OrderItem.objects.filter(
                order__buyer=request.user,
                product=product,
            ).exists()

            review.save()

            messages.success(
                request,
                "Thank you for your review!"
            )

            return redirect(
                "public_product_detail",
                pk=product.id,
            )

    else:

        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "product": product,
        },
    )

def reddit_feed(request):
    """
    Display recent posts from a chosen subreddit.

    This view uses the external API function to fetch
    posts and passes them to the template for rendering.
    """
    # Fetch the latest posts from the "django" subreddit, 
    # limiting to 10 posts.
    posts, api_error = get_reddit_posts(
        subreddit="django", 
        limit=10,
    )

    context = {
        "posts": posts,
        "api_error": api_error,
    }

    return render(
        request,
        "reddit_feed.html",
        context,
    )