from rest_framework import serializers
from recipes.models import Recipe, Tag, Ingredient


class AbstractSerializer(serializers.ModelSerializer):
    pass


class TagSerializer(AbstractSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(AbstractSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    tags = TagSerializer(many=True,)
    ingredients = IngredientSerializer(many=True,)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        ]
