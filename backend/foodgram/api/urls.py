from django.urls import include, path
from rest_framework import routers
from .views import IngredientViewSet, RecipeViewSet, TagViewSet


router = routers.SimpleRouter()

router.register(
    'recipes',
    RecipeViewSet,
    'recipes',
)
router.register(
    'tags',
    TagViewSet,
    'tags',
)
router.register(
    'ingredients',
    IngredientViewSet,
    'ingredients',
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
]
