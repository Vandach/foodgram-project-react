from django.urls import include, path, re_path

from users.views import UserViewSet
from rest_framework import routers
from food.views import RecipeViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'recipe', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/', RecipeViewSet.as_view({"get": "list"})),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
]
