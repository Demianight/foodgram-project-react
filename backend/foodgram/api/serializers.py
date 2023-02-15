from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True,)
    author = UserSerializer(read_only=True,)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        ]


class RecipeCreateSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all()
    )


class SimpleRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'image', 'name', 'cooking_time', ]


# class ShoppingCartSerializer(serializers.Serializer):
#     recipe = serializers.PrimaryKeyRelatedField(
#         queryset=Recipe.objects.all(),
#     )

#     def validate(self, attrs):
#         attrs = super(ShoppingCartSerializer, self).validate(attrs)
#         user = self.context.get('user')
#         recipe = self.context.get('recipe')
#         is_adding = self.context.get('is_adding')

#         if recipe in user.shopping_cart.all() and is_adding:
#             raise serializers.ValidationError(
#                 'This recipe is already in your shopping cart.'
#             )
#         elif recipe not in user.shopping_cart.all() and not is_adding:
#             raise serializers.ValidationError(
#                 'This recipe is not in your shopping cart.'
#             )
#         return attrs

#     def add_to_shopping_cart(self):
#         user = self.context.get('user')
#         recipe = self.context.get('recipe')
#         is_adding = self.context.get('is_adding')
