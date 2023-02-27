# Generated by Django 4.1.6 on 2023-02-27 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_alter_ingredient_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.recipe'),
        ),
    ]