# Generated by Django 4.1.6 on 2023-02-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite',
            field=models.ManyToManyField(to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='user',
            name='shopping_cart',
            field=models.ManyToManyField(related_name='users', to='recipes.recipe'),
        ),
    ]
