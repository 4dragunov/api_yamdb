from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user

class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_staff or \
               request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    '''Только автор может вносить изменения и удалять объект'''
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.role == 'ADMIN'