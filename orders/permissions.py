
from rest_framework import permissions

class IsCustomerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # customer can view their own orders only
        user = request.user
        if hasattr(user, 'customer_profile'):
            return obj.customer.user_id == user.id
        return False

class IsSellerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # simple example: staff user is admin; seller_profile present -> seller
        return user and (user.is_staff or hasattr(user, 'seller_profile'))
