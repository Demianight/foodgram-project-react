from api.pagination import SixItemPagination
from api.views import AbstractGETViewSet
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (ChangePasswordSerializer, FollowSerializer,
                          UserSerializer)


class UsersViewSet(AbstractGETViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = SixItemPagination

    @action(
        detail=False,
        methods=[
            'get',
        ],
        permission_classes=[IsAuthenticated, ],
        url_path='me',
    )
    def get_me(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        data = UserSerializer(user).data
        data['is_subscribed'] = False
        return Response(
            data, status=200
        )

    @action(
        detail=False,
        methods=[
            'post',
        ],
        permission_classes=[IsAuthenticated, ],
        url_path='set_password',
    )
    def set_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=204)

        return Response(serializer.errors, status=400)

    @action(
        detail=True,
        methods=[
            'post', 'delete',
        ],
        permission_classes=[IsAuthenticated, ],
        url_path='subscribe',
    )
    def subscribe(self, request, pk):
        if request.method == 'POST':
            data = {
                'author': pk,
                'follower': request.user.id,
            }
            serializer = FollowSerializer(
                data=data, context={'request': request, }
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    UserSerializer(User.objects.get(id=pk)).data
                )
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            follow = get_object_or_404(Follow, author__id=pk)
            follow.delete()
            return Response(status=204)
