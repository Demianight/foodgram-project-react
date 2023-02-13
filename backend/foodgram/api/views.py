from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import NotAuthPermission

from .serializers import (
    IngredientSerializer, RecipeSerializer,
    RecipeCreateSerializer, TagSerializer
)


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
    permission_classes = [NotAuthPermission]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        url_path='favourite',
        methods=['post', 'delete',],
        permission_classes=[IsAuthenticated, ]
    )
    def add_to_favourite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if recipe in request.user.favourite.all():
                return Response(
                    {'errors': 'This recipe already in your favourite list.'},
                    status=400
                )
            request.user.favourite.add(recipe)
            data = {
                'id': recipe.id,
                # 'image': recipe.image,
                'name': recipe.name,
                'cooking_time': recipe.cooking_time
            }
            return Response(data, status=200)
        if recipe not in request.user.favourite.all():
            return Response(
                {'errors': 'There is no such recipe in your favourite list.'},
                status=400
            )
        request.user.favourite.remove(recipe)
        return Response(status=204)

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=['post', 'delete',],
        permission_classes=[IsAuthenticated, ]
    )
    def add_to_shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if recipe in request.user.shopping_cart.all():
                return Response(
                    {'errors': 'This recipe already in your cart.'},
                    status=400
                )
            request.user.shopping_cart.add(recipe)
            data = {
                'id': recipe.id,
                # 'image': recipe.image,
                'name': recipe.name,
                'cooking_time': recipe.cooking_time
            }
            return Response(data, status=200)
        if recipe not in request.user.shopping_cart.all():
            return Response(
                {'errors': 'There is no such recipe in your cart.'},
                status=400
            )
        request.user.shopping_cart.remove(recipe)
        return Response(status=204)
