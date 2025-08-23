from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission: only owners can edit/delete.
    Safe methods (GET, HEAD, OPTIONS) are allowed for any request.
    """

    def has_permission(self, request, view):
        # allow authenticated users to create; allow anyone to list/retrieve
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the owner/author
        # Works for Post and Comment (both have 'author' field)
        owner = getattr(obj, "author", None)
        return owner == request.user
