from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for everyone.
    Only the author of a post or comment can edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Safe methods like GET, HEAD, OPTIONS are allowed for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise, check if the user is the author
        return getattr(obj, 'author', None) == request.user
