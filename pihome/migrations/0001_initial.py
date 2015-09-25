# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cronjobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobdescription', models.CharField(max_length=250, unique=True)),
                ('whattodo', models.CharField(max_length=10)),
                ('startdate', models.DateField()),
                ('starttime', models.TimeField()),
                ('enddate', models.DateField(blank=True, null=True)),
                ('endtime', models.TimeField(blank=True, null=True)),
                ('periodicity', models.CharField(choices=[('once', 'Only 1 time'), ('daily', 'Every day'), ('weekly', 'Every week'), ('monthly', 'Every month'), ('yearly', 'Every year')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=250)),
                ('systemcode', models.CharField(max_length=10)),
                ('devicecode', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='cronjobs',
            name='deviceid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pihome.devices'),
        ),
    ]
