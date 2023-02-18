# Generated by Django 4.1.6 on 2023-02-16 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_ingredientamount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientamount',
            name='ingredient',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='amount',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredientamount'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='ingredientamount',
            name='recipe',
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.recipe'),
        ),
    ]
