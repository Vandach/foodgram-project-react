from rest_framework import permissions


class IsSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.id == user
            or user.is_authenticated
            and user.is_admin
        )
