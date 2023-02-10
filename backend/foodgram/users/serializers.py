from rest_framework import serializers
from recipes.models import User_model
from .models import ShoppingCart, Favourite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_model
        fields = ['email', 'id', 'username', 'first_name', 'last_name',]


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'
