from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime


# Create your models here.
class devices(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250)
    systemcode = models.CharField(max_length=10)
    devicecode = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add = True)
    status = models.BooleanField(default = 0)

class cronjobs(models.Model):
    PeridodicityChoices = (
        ('once', 'Only 1 time'),
        ('daily', 'Every day'),
        ('weekly', 'Every week'),
        ('monthly', 'Every month'),
        ('yearly', 'Every year'),
    )
    deviceid = models.ForeignKey(devices)
    jobdescription = models.CharField(max_length=250, unique=True)
    whattodo = models.CharField(max_length=10)
    startdate = models.DateField()
    starttime = models.TimeField()
    enddate = models.DateField(null=True, blank=True)
    endtime = models.TimeField(null=True, blank=True)
    periodicity = models.CharField(max_length=50, choices=PeridodicityChoices)


