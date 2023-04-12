from django.contrib import admin

# from .models import Recipe, Category, Recipe2
from .models import Recipe, Product, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    # list_filter = ('time_create',)
    # prepopulated_fields = {'slug': ('title',)}


admin.site.register(Recipe, RecipeAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Product, RecipeAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Tag, RecipeAdmin)

# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
#     list_display_links = ('id', 'title')
#     search_fields = ('title', 'content')
#     list_editable = ('is_published',)
#     list_filter = ('is_published', 'time_create')
#     prepopulated_fields = {'slug': ('title',)}


# class CategotyAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)
#     prepopulated_fields = {'slug': ('name',)}


# class Recipe2Admin(admin.ModelAdmin):
#     list_display = ('id', 'title')
#     list_display_links = ('id', 'title')


# admin.site.register(Recipe2, Recipe2Admin)

# admin.site.register(Recipe, RecipeAdmin)

# admin.site.register(Category, CategotyAdmin)
