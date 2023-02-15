from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name']
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True,)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
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

    def validate_author(self, value):
        user = self.context['request'].user
        print(user)
        if value == user:
            raise serializers.ValidationError(
                'You cannot subscribe on yourself.'
            )
        return value
