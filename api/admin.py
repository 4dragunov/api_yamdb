# from django.contrib import admin
# # из файла models импортируем модель Post
# from .models import Category, Genre, Title
#
# #
#
# class GenreInline(admin.TabularInline):
#     model = Genre
#     extra = 1
#
#
# class TitleAdmin(admin.ModelAdmin):
#     list_display = ("year", "rating", "description",
#                     "category", "slug",)
#     inlines = [GenreInline]
# #
# # # admin.site.register(Category)
# admin.site.register(Title, TitleAdmin)
# # admin.site.register(Genre, GenreAdmin)
