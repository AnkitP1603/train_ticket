# Generated by Django 5.0.7 on 2024-11-02 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_traincarriage_base_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='price',
        ),
    ]