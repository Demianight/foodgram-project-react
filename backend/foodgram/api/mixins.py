from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from recipes.models import Recipe
from users.serializers import CartSerializer, SimpleRecipeSerializer


class AbstractGETViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    pass


# Prev functions still was kinda similar to each other
# In my opinion it looks much better
# Also takes less space and much more DRY
class Cart:
    def __init__(self, pk, request, cart_name) -> None:
        self.pk = pk
        self.request = request
        self.cart_name = cart_name
        self.recipe = get_object_or_404(Recipe, id=pk)
        self.data = {'recipe': self.pk, 'attr': self.cart_name}
        self.serializer = CartSerializer(
            data=self.data,
            context={'request': self.request}
        )
        self.serializer.is_valid(raise_exception=True)

    def add(self):
        self.serializer.save()
        recipe_sr = SimpleRecipeSerializer(self.recipe)
        return Response(recipe_sr.data, status=201)

    def remove(self):
        self.serializer.destroy(self.recipe)
        return Response(status=204)
