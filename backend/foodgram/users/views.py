from rest_framework import mixins
from api.views import AbstractGETViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UsersViewSet(AbstractGETViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
