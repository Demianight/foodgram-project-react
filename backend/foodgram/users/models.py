from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='users'
    )
    favourite = models.ManyToManyField(
        'recipes.Recipe',
    )
