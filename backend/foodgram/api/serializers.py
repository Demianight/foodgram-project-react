from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from users.serializers import UserSerializer


class AbstractSerializer(serializers.ModelSerializer):
    pass


class TagSerializer(AbstractSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(AbstractSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeSerializer(AbstractSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True,)
    ingredients = IngredientSerializer(many=True,)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        ]
