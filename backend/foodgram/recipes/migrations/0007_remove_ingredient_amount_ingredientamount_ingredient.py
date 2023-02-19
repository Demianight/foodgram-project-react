# Generated by Django 4.1.6 on 2023-02-16 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_ingredient_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='amount',
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.ingredient'),
        ),
    ]
