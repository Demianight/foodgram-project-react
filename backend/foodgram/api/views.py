from recipes.models import Ingredient, Recipe, Tag
from rest_framework import mixins, viewsets
from users.permissions import NotAuthPermission

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from users.models import Favourite
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


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
        methods=['post',],
        permission_classes=[IsAuthenticated,]
    )
    def add_to_favourite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        try:
            favour = Favourite.objects.get(owner=request.user, recipe=recipe)
        except Exception:
            favour = Favourite.objects.create(owner=request.user)
            favour.recipe.add(recipe)

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
        raise ValidationError(
            'You cant add recipe to your favourite twice.'
        )
