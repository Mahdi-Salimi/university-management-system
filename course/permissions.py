from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions

class DefaultPermissionOrAnonReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to anonymous users and enforce
    Django's default model permissions for authenticated users.
    """
    def has_permission(self, request, view):
        # Allow read-only access for anonymous users
        if request.method in SAFE_METHODS:
            return True
        
        # Enforce default Django model permissions for authenticated users
        if request.user and request.user.is_authenticated:
            return DjangoModelPermissions().has_permission(request, view)
        
        return False