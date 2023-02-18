from recipes.models import Ingredient, Recipe, Tag
from rest_framework import mixins, viewsets
from users.permissions import NotAuthPermission, IsAuthorPermission

from .pagination import SixItemPagination
from .serializers import (
    IngredientSerializer, RecipeEditCreateSerializer, RecipeSerializer,
    TagSerializer,
)
from rest_framework.decorators import action
from users.serializers import CartSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.serializers import SimpleRecipeSerializer


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
        if self.action == 'partial_update':
            return [IsAuthorPermission(), ]
        return [NotAuthPermission(), ]

    # This actions work, but there are absolutely
    # same and probly could be done better somehow using DRY
    @action(
        detail=True,
        methods=['POST', ],
        url_path='shopping_cart',
    )
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
