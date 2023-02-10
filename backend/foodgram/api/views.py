from recipes.models import Ingredient, Recipe, Tag
from rest_framework import mixins, viewsets
from users.permissions import NotAuthPermission

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


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
