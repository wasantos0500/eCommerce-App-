from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .api_permissions import IsVendor

from .models import Product, Store, Review
from .serializers import (
    ProductSerializer, 
    StoreSerializer,
    ReviewSerializer
)


@api_view(["GET"])
def api_home(request):
    """
    Provide a simple endpoint to confirm that
    Django REST Framework is correctly configured.
    """

    return Response({
        "message": "eCommerce API is working!",
        "status": "success",
    })


@api_view(["GET", "POST"])
def product_list_api(request):
    """
    Retrieve available products or create a new product.

    GET requests are available publicly.

    POST requests are restricted to authenticated vendors.
    Vendors may only create products inside stores that
    belong to their own account.
    """

    # ---------------------------------------------------------
    # GET: Retrieve products available in the marketplace.
    # ---------------------------------------------------------
    if request.method == "GET":

        products = Product.objects.filter(
            available=True
        ).order_by("name")

        serializer = ProductSerializer(
            products,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    # ---------------------------------------------------------
    # POST: Create a product.
    # ---------------------------------------------------------

    # The user must first be authenticated.
    if not request.user.is_authenticated:
        return Response(
            {
                "detail": "Authentication is required to create a product."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Only users belonging to the Vendor group may create products.
    if not request.user.groups.filter(name="Vendor").exists():
        return Response(
            {
                "detail": "Only vendors can create products."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ProductSerializer(
        data=request.data,
        context={"request": request},
    )

    if serializer.is_valid():

        # Retrieve the store selected in the validated request.
        store = serializer.validated_data["store"]

        # Prevent a vendor from adding products to another
        # vendor's store.
        if store.owner != request.user:
            return Response(
                {
                    "detail": (
                        "You can only create products "
                        "inside stores that you own."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # The store ownership check has passed,
        # so the product can safely be created.
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    # Return validation errors if the submitted product
    # data does not satisfy the Product model requirements.
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )

@api_view(["GET", "POST"])
def store_list_api(request):
    """
    Retrieve all stores or create a new store.

    GET requests are available for browsing stores.

    POST requests are restricted to authenticated vendors.
    The authenticated vendor automatically becomes the
    owner of the newly created store.
    """

    # GET requests retrieve all stores.
    if request.method == "GET":

        stores = Store.objects.all().order_by("name")

        serializer = StoreSerializer(
            stores,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    # POST requests require an authenticated vendor.
    if not request.user.is_authenticated:
        return Response(
            {
                "detail": "Authentication is required to create a store."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not request.user.groups.filter(name="Vendor").exists():
        return Response(
            {
                "detail": "Only vendors can create stores."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = StoreSerializer(
        data=request.data,
        context={"request": request},
    )

    if serializer.is_valid():

        # The owner is taken from the authenticated user rather
        # than allowing the client to choose another user.
        serializer.save(
            owner=request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )

@api_view(["GET"])
def store_detail_api(request, pk):
    """
    Return the details of one specific store.

    The store is identified by its primary key supplied
    as part of the API URL.
    """

    store = get_object_or_404(
        Store,
        pk=pk,
    )

    serializer = StoreSerializer(
        store,
        context={"request": request},
    )

    return Response(serializer.data)


@api_view(["GET"])
def product_detail_api(request, pk):
    """
    Return one available product through the REST API.

    Only products currently marked as available are
    exposed through this public endpoint.
    """

    product = get_object_or_404(
        Product,
        pk=pk,
        available=True,
    )

    serializer = ProductSerializer(
        product,
        context={"request": request},
    )

    return Response(serializer.data)

@api_view(["GET"])
def store_products_api(request, pk):
    """
    Return all available products belonging to a specific store.
    """

    # Confirm that the requested store exists.
    store = get_object_or_404(
        Store,
        pk=pk,
    )

    products = store.products.filter(
        available=True
    ).order_by("name")

    serializer = ProductSerializer(
        products,
        many=True,
        context={"request": request},
    )

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsVendor])
def review_list_api(request):
    """
    Return reviews for products belonging to the
    authenticated vendor's stores.

    Vendors must not be able to retrieve reviews belonging
    to products sold by other vendors.
    """

    reviews = Review.objects.filter(
        product__store__owner=request.user
    ).select_related(
        "product",
        "reviewer",
    ).order_by("-created_at")

    serializer = ReviewSerializer(
        reviews,
        many=True,
        context={"request": request},
    )

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsVendor])
def product_reviews_api(request, pk):
    """
    Return reviews for one of the authenticated
    vendor's products.

    The ownership filter prevents a vendor from retrieving
    reviews for another vendor's product through this endpoint.
    """

    product = get_object_or_404(
        Product,
        pk=pk,
        store__owner=request.user,
    )

    reviews = product.reviews.all().order_by(
        "-created_at"
    )

    serializer = ReviewSerializer(
        reviews,
        many=True,
        context={"request": request},
    )

    return Response(serializer.data)