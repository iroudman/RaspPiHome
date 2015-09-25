from django.contrib import admin

from pihome.models import devices
from pihome.models import cronjobs


admin.site.register(devices)
admin.site.register(cronjobs)
