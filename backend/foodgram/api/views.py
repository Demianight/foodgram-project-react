from rest_framework import viewsets
from recipes.models import Recipe, Tag, Ingredient
from .serializers import (
    RecipeSerializer, TagSerializer, IngredientSerializer
)
from users.permissions import NotAuthPermission
from rest_framework import mixins


class AbstractViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [NotAuthPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(AbstractViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(AbstractViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
