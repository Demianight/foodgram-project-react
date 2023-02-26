from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from users.serializers import CartSerializer

from .serializers import SimpleRecipeSerializer


class AbstractGETViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    pass


def add_to_cart(pk, request, cart_name):
    recipe = get_object_or_404(Recipe, id=pk)
    data = {'recipe': pk, 'attr': cart_name}
    serializer = CartSerializer(
        data=data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    recipe_sr = SimpleRecipeSerializer(recipe)
    return Response(recipe_sr.data, status=201)


def remove_from_cart(pk, request, cart_name):
    recipe = get_object_or_404(Recipe, id=pk)
    data = {'recipe': pk, 'attr': cart_name}
    serializer = CartSerializer(
        data=data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.destroy(recipe)
    return Response(status=204)
