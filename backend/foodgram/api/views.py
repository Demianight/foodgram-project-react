from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Favourite, ShoppingCart
from users.permissions import NotAuthPermission

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


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
    serializer_class = RecipeSerializer
    permission_classes = [NotAuthPermission]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        detail=True,
        url_path='favourite',
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def favourite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        favourite = Favourite.objects.get_or_create(owner=request.user)[0]
        if request.method == 'POST':
            favourite.recipe.add(recipe)

            data = {
                'id': recipe.id,
                # 'image': recipe.image,
                'name': recipe.name,
                'cooking_time': recipe.cooking_time,
            }
            return Response(
                data,
                status=201
            )
        else:
            favourite.recipe.remove(recipe)
            return Response(status=204)

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = ShoppingCart.objects.get_or_create(
            owner=request.user
        )[0]
        if request.method == 'POST':
            shopping_cart.recipe.add(recipe)

            data = {
                'id': recipe.id,
                # 'image': recipe.image,
                'name': recipe.name,
                'cooking_time': recipe.cooking_time,
            }
            return Response(
                data,
                status=201
            )
        else:
            shopping_cart.recipe.remove(recipe)
            return Response(status=204)
