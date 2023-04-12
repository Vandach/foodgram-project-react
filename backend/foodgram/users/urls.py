from django.urls import path, include, re_path

from users.views import index

urlpatterns = [
    path('', index),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
