# Generated by Django 3.2 on 2022-02-28 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20220218_1856'),
        ('contact', '0002_contactus_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.userprofile'),
        ),
    ]