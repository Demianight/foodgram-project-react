from api.pagination import SixItemPagination
from api.views import AbstractGETViewSet
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UsersViewSet(AbstractGETViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = SixItemPagination

    @action(
        detail=False,
        methods=['GET',],
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
