from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='users'
    )
    favourite = models.ManyToManyField(
        'recipes.Recipe',
    )
