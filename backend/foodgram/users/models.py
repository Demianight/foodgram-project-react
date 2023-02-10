from django.db import models
from recipes.models import User_model, Recipe


class ShoppingCart(models.Model):
    owner = models.ForeignKey(
        User_model,
        on_delete=models.SET_NULL,
        related_name='cart',
        null=True,
    )
    recipes = models.ManyToManyField(
        Recipe,
    )


class Favourite(models.Model):
    owner = models.ForeignKey(
        User_model,
        on_delete=models.SET_NULL,
        related_name='favourite',
        null=True,
    )
    recipe = models.ManyToManyField(
        Recipe,
    )
