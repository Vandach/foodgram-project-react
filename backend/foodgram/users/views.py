from rest_framework import viewsets
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
