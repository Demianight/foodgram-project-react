from django.contrib.auth.password_validation import validate_password
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        ]
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        follows = user.follows
        ids = follows.values_list('author_id', flat=True)
        if obj.id in ids:
            return True
        return False

    def create(self, validated_data):
        password = self.initial_data.pop('password')
        user: User = super().create(validated_data)
        try:
            validate_password(password)
            user.set_password(password)
            user.save()
            return user
        except serializers.ValidationError as exc:
            user.delete()
            raise exc


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True,)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Wrong old password.'
            )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('author', 'follower')
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['follower', 'author']
            )
        ]

    def validate_author(self, author):
        user = self.context.get('request').user
        if author == user:
            raise serializers.ValidationError(
                'You cannot subscribe on yourself.'
            )
        return author


class CartSerializer(serializers.Serializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )
    attr = serializers.CharField()

    def destroy(self, recipe):
        user = self.context.get('request').user
        recipe = self.validated_data.get('recipe')
        attr = self.validated_data.get('attr')
        cart = getattr(user, attr)
        if recipe not in cart.all():
            raise serializers.ValidationError(
                'This recipe is already removed.'
            )
        cart.remove(recipe)
        return {}

    def create(self, validated_data):
        user = self.context.get('request').user
        recipe = validated_data.get('recipe')
        attr = validated_data.get('attr')
        cart = getattr(user, attr)
        if recipe in cart.all():
            raise serializers.ValidationError(
                'This recipe is already added.'
            )
        cart.add(recipe)

        return recipe
