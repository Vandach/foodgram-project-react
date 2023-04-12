from django.urls import path, include, re_path

from users.views import UserViewSet

urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
