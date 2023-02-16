# Generated by Django 4.1.1 on 2022-10-17 11:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('login', models.CharField(max_length=30, unique=True)),
                ('role', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('password', models.CharField(max_length=16)),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
    ]