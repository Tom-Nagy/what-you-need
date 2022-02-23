# Generated by Django 3.2 on 2022-02-22 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_auto_20220218_1856'),
        ('products', '0012_alter_productreview_review_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='My whislist', max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whislist', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to='wishlists.wishlist')),
            ],
        ),
    ]