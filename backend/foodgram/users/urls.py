from django.urls import path, include, re_path
from .views import UpdatePassword


urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('set_password/', UpdatePassword.as_view()),
]
