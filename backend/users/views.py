from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsSelf

from .models import Follow, User
from .serializers import (ChangePasswordSerializer, FollowSerializer,
                          SubscribeSerializer, UserCreateSerializer,
                          UserSerializer)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):

        user = request.user
        users = Follow.objects.filter(user=user)
        page = self.paginate_queryset(users)
        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request}
            )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        if request.method == 'POST':
            return self.add_to(request, Follow, request.user, pk)
        else:
            return self.delete_from(Follow, request.user, pk)

    def add_to(self, request, model, user, pk):
        if model.objects.filter(user=user, author__id=pk).exists():
            return Response({'errors': 'Вы уже подписаны!'},
                            status=status.HTTP_400_BAD_REQUEST)
        author = get_object_or_404(User, id=pk)
        if author == user:
            return Response({'errors': 'Нельзя подписаться на самого себя!'},
                            status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, author_id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы уже отписаны!'},
                        status=status.HTTP_400_BAD_REQUEST)

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
