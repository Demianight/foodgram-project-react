from api.pagination import SixItemPagination
from api.views import AbstractGETViewSet
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import (ChangePasswordSerializer, FollowSerializer,
                          UserSerializer, UserWithRecipesSerializer)


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
        data = UserSerializer(
            user,
            context={
                'request': request
            }
        ).data
        return Response(
            data, status=200
        )

    @action(
        detail=False,
        methods=[
            'POST',
        ],
        permission_classes=[IsAuthenticated, ],
        url_path='set_password',
    )
    def set_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response(status=204)

    @action(
        detail=True,
        methods=['POST', ],
        permission_classes=[IsAuthenticated, ],
        url_path='subscribe',
    )
    def subscribe(self, request, pk):
        data = {
            'author': pk,
            'follower': request.user.id,
        }
        serializer = FollowSerializer(
            data=data, context={'request': request, }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipes_count = self.request.query_params.get('recipes_count', 99999)

        return Response(
            UserWithRecipesSerializer(
                User.objects.get(id=pk), context={
                    'request': request,
                    'recipes_count': recipes_count
                }
            ).data
        )

    @subscribe.mapping.delete
    def delete_follow(self, request, pk=None):
        follow = request.user.follows.filter(author__id=pk)
        if follow:
            follow.delete()
            return Response(status=204)
        raise ValidationError(
            {'errors': 'You are not subscribed on this person.'}
        )

    @action(
        detail=False,
        methods=['GET', ],
        url_path='subscribtions',
    )
    def subscribtions(self, request):
        follows = request.user.follows.all()
        ids = follows.values_list('author_id', flat=True)
        queryset = User.objects.filter(id__in=ids)
        recipes_count = self.request.query_params.get('recipes_count', 99999)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserWithRecipesSerializer(
                page, many=True, context={
                    'recipes_count': recipes_count,
                    'request': request
                }
            )
            return self.get_paginated_response(serializer.data)

        serializer = UserWithRecipesSerializer(
            queryset, many=True, context={
                'recipes_count': recipes_count,
                'request': request
            }
        )

        serializer.is_valid()
        return Response(serializer.data)
