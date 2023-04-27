from django.urls import include, path, re_path

from users.views import UserViewSet
from rest_framework import routers
from food.views import (RecipeViewSet, TagsViewSet,
                        IngredientViewSet, RecipeIngredientsViewSet, test)
from users.views import UpdatePassword

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'ringredients', RecipeIngredientsViewSet)
router.register(r'test', test)

urlpatterns = [
    path('users/set_password/', UpdatePassword.as_view()),
    path('', include(router.urls)),
    path('recipe/', RecipeViewSet.as_view({"get": "list", 'post': 'create'
                                            })),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
]
