from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# from .models import Recipe, Category, Recipe2
from .models import Recipe, Product, Tag, Enrollment
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User as DjangoUser

# class CustomUserAdmin(UserAdmin):
#     list_display = ('USER', 'MODERATOR', 'ADMIN', 'USER_ROLES', 'email')
#     # list_filter = ('MODERATOR', 'ADMIN')
#     search_fields = ('email',)
#     ordering = ('email',)

# admin.site.register(User, CustomUserAdmin)


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


# class UserAdmin(User):
#     list_display = ('USER', 'MODERATOR', 'ADMIN', 'USER_ROLES')


# admin.site.unregister(du)
# admin.site.register(User, UserAdmin)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)


# admin.site.register(Product, ProductAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Tag, TagAdmin)

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
