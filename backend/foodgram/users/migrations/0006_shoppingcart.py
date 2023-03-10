# Generated by Django 4.1.6 on 2023-02-16 12:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_remove_ingredient_amount_ingredientamount_ingredient'),
        ('users', '0005_remove_user_favourite_remove_user_shopping_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL)),
                ('recipes', models.ManyToManyField(to='recipes.recipe')),
            ],
        ),
    ]
