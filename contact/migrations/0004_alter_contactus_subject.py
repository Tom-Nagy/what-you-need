# Generated by Django 3.2 on 2022-02-28 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_contactus_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='subject',
            field=models.CharField(choices=[('Information', 'Information'), ('Issue', 'Issue'), ('Other', 'Other')], default='Information', max_length=254),
        ),
    ]
