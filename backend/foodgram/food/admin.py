from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Enrollment, Product, Recipe, Tag


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInline]
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    # list_filter = ('time_create',)
    # prepopulated_fields = {'slug': ('title',)}


admin.site.register(Recipe, RecipeAdmin)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource


admin.site.register(Product, ProductAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Tag, TagAdmin)
