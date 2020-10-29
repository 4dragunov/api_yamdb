from django.contrib import admin
# из файла models импортируем модель Post
from .models import User

admin.site.register(User)