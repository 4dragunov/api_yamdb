from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class IsOwnerOrReadOnly(BasePermission):
    '''Только автор может вносить изменения и удалять объект'''
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user




class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.role == 'ADMIN' or request.user.is_staff or request.user.is_superuser

    # is_superuser