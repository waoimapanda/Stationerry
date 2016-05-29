# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 05:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('App_Name', models.TextField()),
                ('App_Version', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Error_Type', models.TextField()),
                ('Error_Message', models.TextField()),
                ('Date', models.DateField()),
                ('Time', models.TimeField()),
                ('Platform', models.TextField()),
                ('App_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Name', to='StationerryBackend.App')),
                ('App_Version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Version', to='StationerryBackend.App')),
            ],
        ),
    ]
