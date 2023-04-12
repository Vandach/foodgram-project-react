from django.urls import path

from users.views import UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),

]
