from .models import User
from rest_framework import serializers


"""HAVE TO REWRITE IT"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
