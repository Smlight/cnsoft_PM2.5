# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-21 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beijing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chengdu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pres', models.IntegerField()),
                ('tmp', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_sc', models.CharField(max_length=30)),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
                ('suggestion', models.CharField(max_length=3000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Guangzhou',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hangzhou',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nanjing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMBeijing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMChengdu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMGuangzhou',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMHangzhou',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMNanjing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMShanghai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMShenzhen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMTianjin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMWuhan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PMXian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Realtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('time', models.DateTimeField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pres', models.IntegerField()),
                ('tmp', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_dir', models.CharField(max_length=30)),
                ('wind_sc', models.CharField(max_length=30)),
                ('aqi', models.IntegerField()),
                ('aqi_str', models.CharField(max_length=30)),
                ('pm25', models.IntegerField()),
                ('suggestion', models.CharField(max_length=3000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shanghai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shenzhen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tianjin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wuhan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Xian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cond', models.CharField(max_length=30)),
                ('hum', models.IntegerField()),
                ('pcpn', models.FloatField()),
                ('pres', models.IntegerField()),
                ('tmp_max', models.IntegerField()),
                ('tmp_min', models.IntegerField()),
                ('vis', models.IntegerField()),
                ('wind_deg', models.IntegerField()),
                ('wind_spd', models.IntegerField()),
                ('aqi', models.IntegerField()),
                ('pm25', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
