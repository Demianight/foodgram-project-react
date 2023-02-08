from django.urls import include, path
from rest_framework import routers

from .views import (
    TagViewSet, RecipeViewSet, IngredientViewSet
)


router = routers.SimpleRouter()

router.register(
    'recipes',
    RecipeViewSet,
)
router.register(
    'tags',
    TagViewSet,
)
router.register(
    'ingredients',
    IngredientViewSet,
)

urlpatterns = [
    path('', include(router.urls)),
]
