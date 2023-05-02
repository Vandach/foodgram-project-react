from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                     ShoppingCart, Tag)


class RecipeIngredients(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredients]
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('title', 'content')


admin.site.register(Recipe, RecipeAdmin)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Ingredient


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource


admin.site.register(Ingredient, ProductAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')
    search_fields = ('name',)


admin.site.register(ShoppingCart, ShoppingCartAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')
    search_fields = ('name',)


admin.site.register(Favorite, FavoriteAdmin)
