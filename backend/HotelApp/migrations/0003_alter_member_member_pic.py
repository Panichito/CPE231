# Generated by Django 4.0.4 on 2022-05-07 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelApp', '0002_member_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='Member_Pic',
            field=models.ImageField(blank=True, null=True, upload_to=None),
        ),
    ]
