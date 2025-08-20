from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsReviewAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        
        return obj.user == request.user

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow safe (read-only) methods for everyone
        if request.method in SAFE_METHODS:
            return True
        # Allow write methods only for admin users
        return request.user and request.user.is_staff