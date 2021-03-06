# Generated by Django 3.2 on 2022-02-21 19:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20220218_1856'),
        ('products', '0010_alter_productreview_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productreview',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.userprofile'),
        ),
    ]
