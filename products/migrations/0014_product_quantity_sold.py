# Generated by Django 3.2 on 2022-02-25 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_sold',
            field=models.PositiveIntegerField(default=0),
        ),
    ]