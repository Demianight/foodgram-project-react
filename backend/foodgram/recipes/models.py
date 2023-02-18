from colorfield.fields import ColorField
from django.db import models
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
    )
    name = models.CharField(max_length=128, )
    image = models.ImageField(upload_to='recipes/', )
    text = models.TextField()
    ingredients = models.ManyToManyField('Ingredient', )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
    )
    cooking_time = models.SmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True, )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64, )
    color = ColorField(default='#FF0000', )
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128, )
    measurement_unit = models.CharField(max_length=32, )

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.SmallIntegerField()

    def __str__(self):
        return str(self.amount)
