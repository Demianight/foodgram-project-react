from dataclasses import dataclass

from rest_framework import viewsets

from .views import IngredientViewSet, RecipeViewSet, TagViewSet


@dataclass
class RouterContainer:
    router_endpoint: str
    viewset_class: viewsets.GenericViewSet
    basename: str


router_data = [
    RouterContainer('recipes', RecipeViewSet, 'recipes'),
    RouterContainer('tags', TagViewSet, 'tags',),
    RouterContainer('ingredients', IngredientViewSet, 'ingredients'),
]
