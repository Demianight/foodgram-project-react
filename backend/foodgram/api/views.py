from urllib.parse import unquote

from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import NotAuthPermission

from .mixins import AbstractGETViewSet, add_to_cart, remove_from_cart
from .pagination import SixItemPagination
from .serializers import (IngredientSerializer, RecipeEditCreateSerializer,
                          RecipeSerializer, TagSerializer)
from .utils import make_cart_file


class TagViewSet(AbstractGETViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(AbstractGETViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')

        if name:
            if name[0] == '%':
                name = unquote(name)
            name = name.lower()
        return list(queryset.filter(name__istartswith=name))


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = SixItemPagination
    permission_classes = [NotAuthPermission, ]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeEditCreateSerializer
        return RecipeSerializer

    # def get_permissions(self):
    #     if self.action in ('partial_update', 'delete'):
    #         return [IsAuthorPermission(), ]
    #     return [NotAuthPermission(), ]

    def get_queryset(self):
        queryset = self.queryset

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        # Only for auth users
        if not self.request.user.is_authenticated:
            return queryset

        is_in_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_in_cart:
            ids = self.request.user.shopping_cart.values_list('id', flat=True)
            queryset = queryset.filter(id__in=ids)

        is_in_favorite = self.request.query_params.get('is_in_favorite')
        if is_in_favorite:
            ids = self.request.user.favorite.values_list('id', flat=True)
            queryset = queryset.filter(id__in=ids)

        return queryset

    @action(detail=True, methods=['POST', ], url_path='shopping_cart',)
    def shopping_cart(self, request, pk=None):
        return add_to_cart(pk, request, 'shopping_cart')

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        return remove_from_cart(pk, request, 'shopping_cart')

    @action(detail=True, methods=['POST', ], url_path='favorite', )
    def favorite(self, request, pk=None):
        return add_to_cart(pk, request, 'favorite')

    @favorite.mapping.delete
    def remove_favorite_list(self, request, pk=None):
        return remove_from_cart(pk, request, 'favorite')

    @action(
        detail=False,
        methods=['GET', ],
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        filename = make_cart_file(request.user)

        file = open(filename, 'r')

        response: Response = Response(
            file, content_type='text/plain',
        )
        response['Content-Disposition'] = 'attachment; filename="text.txt"'
        return response
