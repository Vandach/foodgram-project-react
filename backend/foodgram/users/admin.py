# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User as DjangoUser
# from .models import User


# # UserAdmin.fieldsets += ('Custom fields', {'fields': ('email',)}),


# class CustomUserAdmin(UserAdmin):
#     list_display = ('USER', 'MODERATOR', 'ADMIN', 'USER_ROLES', 'email')
#     # list_filter = ('MODERATOR', 'ADMIN')
#     search_fields = ('email',)
#     ordering = ('email',)

# # admin.site.unregister(DjangoUser)
# admin.site.register(User, CustomUserAdmin)
