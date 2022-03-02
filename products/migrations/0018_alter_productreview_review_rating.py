# Generated by Django 3.2 on 2022-03-02 06:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_product_selling_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='review_rating',
            field=models.PositiveSmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]