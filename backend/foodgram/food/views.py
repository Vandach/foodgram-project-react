from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import viewsets


from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
