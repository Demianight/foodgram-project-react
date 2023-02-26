from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='users',
        blank=True,
    )
    favorite = models.ManyToManyField(
        'recipes.Recipe',
        blank=True,
    )


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follows',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author', ],
                name='Unique follow'
            )
        ]
