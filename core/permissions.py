from rest_framework import permissions



class IsOwner(permissions.BasePermission):
    """
    
    """

    def has_object_permission(self, request, view, obj):
        try:
            token = request.headers['Authorization']
        except KeyError:
            return False

        return obj.auth_token.__str__() == token
