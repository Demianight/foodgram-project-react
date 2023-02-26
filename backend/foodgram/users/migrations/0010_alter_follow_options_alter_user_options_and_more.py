# Generated by Django 4.1.6 on 2023-02-26 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_alter_ingredient_options_and_more'),
        ('users', '0009_rename_favourite_user_favorite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписка'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователь'},
        ),
        migrations.AlterField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favorite',
            field=models.ManyToManyField(blank=True, to='recipes.recipe', verbose_name='Лист избранного'),
        ),
        migrations.AlterField(
            model_name='user',
            name='shopping_cart',
            field=models.ManyToManyField(blank=True, related_name='users', to='recipes.recipe', verbose_name='Корзина покупок'),
        ),
    ]
