from django.contrib import admin
# из файла models импортируем модель Post
from .models import Category, Genre, Title

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)