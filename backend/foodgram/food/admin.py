from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import RecipeIngredients, Ingredient, Recipe, Tag


class EnrollmentInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInline]
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('title', 'content')
    # list_filter = ('time_create',)
    # prepopulated_fields = {'slug': ('title',)}


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
