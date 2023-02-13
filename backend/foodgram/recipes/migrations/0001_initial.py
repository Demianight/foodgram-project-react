# Generated by Django 4.1.6 on 2023-02-13 16:04

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('measurement_unit', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='recipes/')),
                ('text', models.TextField()),
                ('cooking_time', models.SmallIntegerField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None)),
                ('slug', models.SlugField()),
            ],
        ),
    ]
