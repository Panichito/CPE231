# Generated by Django 4.0.4 on 2022-05-13 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HotelApp', '0014_remove_payment_promotion_id_payment_promotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='Transaction_Checkin',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='Transaction_Checkout',
        ),
    ]
