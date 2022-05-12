# Generated by Django 4.0.4 on 2022-05-12 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HotelApp', '0011_rename_hotel_id_staff_hotel_remove_allbook_room_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='Hotel_Id',
        ),
        migrations.RemoveField(
            model_name='room',
            name='Type_Id',
        ),
        migrations.AddField(
            model_name='room',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HotelApp.hotel'),
        ),
        migrations.AddField(
            model_name='room',
            name='roomtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HotelApp.roomtype'),
        ),
    ]
