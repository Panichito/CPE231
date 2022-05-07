# Generated by Django 4.0.4 on 2022-05-07 10:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Room_Id', models.IntegerField()),
                ('Transaction_Id', models.CharField(max_length=12)),
                ('Book_Night', models.IntegerField()),
                ('Book_Price', models.IntegerField()),
            ],
            options={
                'db_table': 'allbook',
            },
        ),
        migrations.CreateModel(
            name='GetNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Member_Id', models.IntegerField()),
                ('News_Id', models.IntegerField()),
            ],
            options={
                'db_table': 'getnews',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hotel_Name', models.CharField(max_length=50)),
                ('Hotel_Address', models.TextField()),
                ('Hotel_Detail', models.TextField(blank=True, null=True)),
                ('Hotel_Pic', models.ImageField(upload_to=None)),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Member_fName', models.CharField(max_length=100)),
                ('Member_lName', models.CharField(max_length=100)),
                ('Member_Email', models.CharField(max_length=100)),
                ('Member_Username', models.CharField(max_length=100)),
                ('Member_Password', models.CharField(max_length=100)),
                ('Member_NIC', models.CharField(max_length=25)),
                ('Member_Address', models.TextField()),
                ('Member_Tel', models.CharField(max_length=25)),
                ('Member_Pic', models.ImageField(upload_to=None)),
                ('Member_Point', models.IntegerField(default=0)),
                ('Staff_Id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('News_Name', models.CharField(max_length=50)),
                ('News_Detail', models.TextField()),
                ('News_Pic', models.ImageField(upload_to=None)),
            ],
            options={
                'db_table': 'news',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Promotion_Id', models.IntegerField()),
                ('Payment_Date', models.DateTimeField()),
                ('Payment_Allprice', models.IntegerField()),
                ('Payment_Vat10', models.IntegerField()),
                ('Payment_Banking', models.CharField(max_length=20)),
                ('Payment_Slip', models.ImageField(upload_to=None)),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Promotion_Discount', models.FloatField()),
                ('Promotion_Start', models.DateTimeField()),
                ('Promotion_End', models.DateTimeField()),
                ('Promotion_Name', models.CharField(max_length=50)),
                ('Promotion_Detail', models.TextField()),
                ('Promotion_Pic', models.ImageField(upload_to=None)),
            ],
            options={
                'db_table': 'promotion',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hotel_Id', models.IntegerField()),
                ('Type_Id', models.IntegerField()),
                ('Room_Number', models.CharField(max_length=20)),
                ('Room_Status', models.BooleanField(default=1)),
            ],
            options={
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type_Name', models.CharField(max_length=50)),
                ('Type_Pernight', models.IntegerField()),
                ('Type_Capacity', models.PositiveSmallIntegerField(default=1)),
                ('Type_Detail', models.TextField()),
                ('Type_Pic', models.ImageField(upload_to=None)),
            ],
            options={
                'db_table': 'roomtype',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Member_Id', models.IntegerField()),
                ('Hotel_Id', models.IntegerField()),
                ('Staff_Position', models.CharField(max_length=50)),
                ('Staff_Start', models.DateField(default=datetime.date.today)),
                ('Staff_End', models.DateField(blank=True, null=True)),
                ('Staff_Level', models.PositiveSmallIntegerField(default=1)),
                ('Staff_Status', models.BooleanField(default=1)),
            ],
            options={
                'db_table': 'staffmanager',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Member_Id', models.IntegerField()),
                ('Payment_Id', models.IntegerField()),
                ('Transaction_Checkin', models.DateTimeField()),
                ('Transaction_Checkout', models.DateTimeField(blank=True, null=True)),
                ('Transaction_Date', models.DateTimeField()),
                ('Transaction_Detail', models.TextField(default='Reserved')),
                ('Transaction_Rating', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('Transaction_Comment', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'transaction',
            },
        ),
    ]
