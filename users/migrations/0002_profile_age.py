# Generated by Django 5.0.7 on 2024-11-04 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]