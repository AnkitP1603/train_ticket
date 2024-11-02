# Generated by Django 5.0.7 on 2024-11-02 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_remove_seat_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]