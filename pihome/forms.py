__author__ = 'igor'

from django import forms
from models import devices, cronjobs

class CreateAddForm(forms.ModelForm):
    class Meta:
        model = devices
        fields = ('id','name','description','systemcode','devicecode')

class CreateAddJobForm(forms.ModelForm):
    class Meta:
        model = cronjobs
        fields = ('id','deviceid','jobdescription','whattodo','startdate','starttime','enddate','endtime','periodicity')


