"""
Custom decorators used to restrict access based on user roles.

These decorators check whether a logged-in user belongs
to the required Django Group.
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def vendor_required(view_func):
    """
    Allow access only to users who belong to the Vendor group.
    """

    @login_required
    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(name="Vendor").exists():
            return view_func(request, *args, **kwargs)

        raise PermissionDenied

    return wrapper


def buyer_required(view_func):
    """
    Allow access only to users who belong to the Buyer group.
    """

    @login_required
    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(name="Buyer").exists():
            return view_func(request, *args, **kwargs)

        raise PermissionDenied

    return wrapper