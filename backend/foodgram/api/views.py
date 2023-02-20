from urllib.parse import unquote

from api.serializers import SimpleRecipeSerializer
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import IsAuthorPermission, NotAuthPermission
from users.serializers import CartSerializer

from .pagination import SixItemPagination
from .serializers import (IngredientSerializer, RecipeEditCreateSerializer,
                          RecipeSerializer, TagSerializer)


class AbstractGETViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    pass


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
            queryset = list(queryset.filter(name__istartswith=name))

        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = SixItemPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeEditCreateSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action in ('partial_update', 'delete'):
            return [IsAuthorPermission(), ]
        return [NotAuthPermission(), ]

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

        is_in_favourite = self.request.query_params.get('is_in_favourite')
        if is_in_favourite:
            ids = self.request.user.favourite.values_list('id', flat=True)
            queryset = queryset.filter(id__in=ids)

        return queryset

    # This actions work, but there are absolutely
    # same and probly could be done better somehow using DRY
    @action(detail=True, methods=['POST', ], url_path='shopping_cart',)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'recipe': pk, 'attr': 'shopping_cart'}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe_sr = SimpleRecipeSerializer(recipe)
        return Response(recipe_sr.data, status=201)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'recipe': pk, 'attr': 'shopping_cart'}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.destroy(recipe)
        return Response(status=204)

    @action(
        detail=True,
        methods=['POST', ],
        url_path='favourite',
    )
    def favourite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'recipe': pk, 'attr': 'favourite'}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe_sr = SimpleRecipeSerializer(recipe)
        return Response(recipe_sr.data, status=201)

    @favourite.mapping.delete
    def remove_favourite_list(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'recipe': pk, 'attr': 'favourite'}
        serializer = CartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.destroy(recipe)
        return Response(status=204)
