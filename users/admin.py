from .models import User

from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "bio", "email", "role")
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)