from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsSelf
from .serializers import (UserSerializer,
                          UserCreateSerializer, ChangePasswordSerializer)
from .models import User
from django.contrib.auth.hashers import check_password
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return UserSerializer
        return UserCreateSerializer

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsSelf]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("current_password")
            new_password = serializer.data.get("new_password")
            checking_password = self.object.password
            matchcheck = check_password(old_password, checking_password)

            if matchcheck is False and old_password != checking_password:
                return Response({f"{old_password}": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(new_password)
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
