# Generated by Django 4.1.6 on 2023-02-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_favourite_user_shopping_cart_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('follower', 'author'), name='Unique follow'),
        ),
    ]
