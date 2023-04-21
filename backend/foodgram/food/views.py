from typing import Any
from requests import Request
from rest_framework.response import Response
from .models import Recipe, User, Tag
from .serializers import (RecipeSerializer, RecipeCreateSerializer,
                          TagSerializer)
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        return RecipeCreateSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=User.objects.get(username=request.user))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TagSerializer
