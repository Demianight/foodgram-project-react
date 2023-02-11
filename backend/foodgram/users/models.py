from django.db import models
from recipes.models import Recipe, User_model


class ShoppingCart(models.Model):
    owner = models.ForeignKey(
        User_model,
        on_delete=models.SET_NULL,
        related_name='cart',
        null=True,
    )
    recipe = models.ManyToManyField(
        Recipe,
    )

    def save(self, *args, **kwargs) -> None:
        self.validate_unique()

        return super().save(*args, **kwargs)


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
