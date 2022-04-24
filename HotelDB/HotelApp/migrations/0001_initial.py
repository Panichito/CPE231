# Generated by Django 4.0.4 on 2022-04-23 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [   # พอมาใช้ MySQL ไม่ได้ทำ makemigration+migrate แล้ว เหมือนมันจะดึงข้อมูลมาจากตัว phpMyAdmin แทน
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hotel_Name', models.TextField()),
                ('Hotel_Address', models.TextField()),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('News_Name', models.CharField(max_length=50)),
                ('News_Detail', models.TextField()),
            ],
            options={
                'db_table': 'news',
            },
        ),
        migrations.CreateModel(
            name='StaffManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hotel_Id', models.CharField(max_length=12)),
                ('Staff_Name', models.CharField(max_length=30)),
                ('Position', models.CharField(max_length=30)),
                ('Start_Date', models.DateField(blank=True, null=True)),
                ('End_Date', models.DateField(blank=True, null=True)),
                ('Degree', models.IntegerField()),
                ('Status', models.BooleanField()),
            ],
            options={
                'db_table': 'staffmanager',
            },
        ),
    ]
