from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from rest_framework import serializers
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug', ]


class IngredientAmountSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )
    ingredient = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = IngredientAmount
        fields = ['ingredient', 'amount', ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit', ]


class IngredientsInRecipesPostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientAmount
        fields = ['id', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True,)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time', 'is_favorited', 'is_in_shopping_cart',
        ]

    def get_ingredients(self, obj: Recipe):
        raw_ingredients = obj.ingredients.all()

        ingredients = []
        for ingredient in raw_ingredients:
            amount = IngredientAmount.objects.get(
                recipe=obj, ingredient=ingredient
            ).amount

            data = IngredientSerializer(ingredient).data
            data['amount'] = amount

            ingredients.append(data)
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj in user.favorite.all()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj in user.shopping_cart.all()
        return False


class RecipeEditCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientsInRecipesPostSerializer(many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time'
        ]

    @staticmethod
    def create_ingredients(ingredients, recipe: Recipe):
        ingredients_amount = [IngredientAmount(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount'],
        ) for ingredient in ingredients]
        IngredientAmount.objects.bulk_create(ingredients_amount)

        recipe.ingredients.set([ingr['id'] for ingr in ingredients])

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredient = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredient, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in self.validated_data:
            tags = validated_data.pop('tags', instance.tags.all())
            instance.tags.set(tags)

        if 'ingredients' in self.validated_data:
            ingredients = validated_data.pop('ingredients')
            IngredientAmount.objects.filter(recipe=instance).delete()
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)

        super().update(instance, validated_data)

        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(
            instance, context=context
        ).data


class SimpleRecipeSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time', ]
