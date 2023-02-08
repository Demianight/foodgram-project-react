from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField


User_model = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User_model,
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(
        max_length=128,
    )
    image = models.ImageField()
    text = models.TextField(
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='ingredients',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tags',
    )
    cooking_time = models.SmallIntegerField(
    )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=64
    )
    color = ColorField(
        default='#FF0000',
    )
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128
    )
    amount = models.SmallIntegerField()
    units = models.CharField(
        max_length=16
    )

    def __str__(self) -> str:
        return self.name
