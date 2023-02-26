from api.pagination import SixItemPagination
from api.views import AbstractGETViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import NotAuthPermission
from .serializers import (ChangePasswordSerializer, FollowSerializer,
                          UserSerializer, UserWithRecipesSerializer)


class UsersViewSet(AbstractGETViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = SixItemPagination
    permission_classes = [NotAuthPermission, ]

    @action(
        detail=False,
        methods=[
            'get',
        ],
        permission_classes=[IsAuthenticated, ],
        url_path='me',
    )
    def get_me(self, request):
        data = UserSerializer(
            request.user,
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
        user.set_password(serializer.validated_data.get('new_password'))
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
        recipes_limit = self.request.query_params.get('recipes_limit', 99999)

        return Response(
            UserWithRecipesSerializer(
                request.user, context={
                    'request': request,
                    'recipes_limit': recipes_limit
                }
            ).data
        )

    @subscribe.mapping.delete
    def delete_follow(self, request, pk=None):
        follow = request.user.follows.filter(author__id=pk)
        if follow.exists():
            follow.delete()
            return Response(status=204)
        raise ValidationError(
            {'errors': 'You are not subscribed on this person.'}
        )

    @action(
        detail=False,
        methods=['GET', ],
        url_path='subscriptions',
    )
    def subscriptions(self, request):
        follows = request.user.follows.all()
        ids = follows.values_list('author_id', flat=True)
        queryset = User.objects.filter(id__in=ids)
        recipes_limit = self.request.query_params.get('recipes_limit', 99999)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserWithRecipesSerializer(
                page, many=True, context={
                    'recipes_limit': recipes_limit,
                    'request': request
                }
            )
            return self.get_paginated_response(serializer.data)

        serializer = UserWithRecipesSerializer(
            queryset, many=True, context={
                'recipes_limit': recipes_limit,
                'request': request
            }
        )

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
