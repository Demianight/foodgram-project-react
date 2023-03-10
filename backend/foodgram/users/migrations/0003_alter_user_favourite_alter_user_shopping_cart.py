# Generated by Django 4.1.6 on 2023-02-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
        ('users', '0002_user_favourite_user_shopping_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favourite',
            field=models.ManyToManyField(blank=True, to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='user',
            name='shopping_cart',
            field=models.ManyToManyField(blank=True, related_name='users', to='recipes.recipe'),
        ),
    ]
