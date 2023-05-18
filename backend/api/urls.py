from django.urls import include, path, re_path
from food.views import IngredientViewSet, RecipeViewSet, TagsViewSet
from rest_framework import routers
from users.views import UpdatePassword, UserViewSet


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('users/set_password/', UpdatePassword.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
