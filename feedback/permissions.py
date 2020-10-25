from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from core.models import User

class TokenMatches(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = request.headers['Authorization']
        except KeyError:
            return False

        return obj.auth_token.__str__() == token



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.headers['Authorization']
            user = User.objects.get(auth_token=token)
        except KeyError:
            return False
        except ObjectDoesNotExist:
            return False

        return user.is_admin