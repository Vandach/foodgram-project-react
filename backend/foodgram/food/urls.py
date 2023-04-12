
# from django.urls import path, re_path, include

# from food.views import (
#     categoties, archive, ShowRecipe, FoodHome,
#     ShowCategory, AddPage, RegisterUser, LoginUser,
#     logout_user, RecipeAPIView
#     )


# urlpatterns = [
#     path('', FoodHome.as_view(), name='home'),
#     path('categoties/<int:catid>/', categoties),
#     re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
#     path('addrecipe/', AddPage.as_view(), name='addrecipe'),
#     path('register/', RegisterUser.as_view(), name='register'),
#     path('login/', LoginUser.as_view(), name='login'),
#     path('logout/', logout_user, name='logout'),
#     path('food/<slug:recipe_slug>', ShowRecipe.as_view(), name='recipe'),
#     path('category/<slug:cat_slug>', ShowCategory.as_view(), name='category'),
#     path('api/v1/recipelist/', RecipeAPIView.as_view()),
#     # path('api/v1/auth/', include('djoser.urls')),
#     # re_path(r'^auth/', include('djoser.urls.authtoken')),
# ]
