from rest_framework.permissions import BasePermission


class IsVendor(BasePermission):
    """
    Allow API access only to authenticated users
    who belong to the Vendor group.
    """

    message = "You must be logged in as a vendor to perform this action."

    def has_permission(self, request, view):
        """
        Check that the user is authenticated and belongs
        to the Vendor group.
        """

        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Vendor").exists()
        )