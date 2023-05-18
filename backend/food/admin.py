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
    readonly_fields = ['count_favorite']
    list_filter = ['name', 'author', 'tags']
    empty_value_display = '-empty-'

    @admin.display(description='Добавлений в Избранное')
    def count_favorite(self, obj):
        return obj.favorite.count()


admin.site.register(Recipe, RecipeAdmin)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Ingredient


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    search_fields = ('name',)
    list_filter = ['name']


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
