# Generated by Django 4.0.6 on 2022-10-10 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='userbase',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
