"""RaspPiHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from pihome import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^getdatatoedit/', views.getdatatoedit, name='getdatatoedit'),
    url(r'^addrecord/', views.addrecord, name='addrecord'),
    url(r'^editrecord/', views.editrecord, name='editrecord'),
    url(r'^deleterecord/([0-9]+)?/$', views.deleterecord, name='deleterecord'),
    url(r'^getlistfromJTable/', views.getlistfromJTable, name='getlistfromJTable'),
    url(r'^verify/', views.verify, name='verify'),
    url(r'^config/', views.config, name='config'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^writeconfig/', views.writeconfig, name='writeconfig'),
    url(r'^addrecordfromJTable/', views.addrecordfromJTable, name='addrecordfromJTable'),
    url(r'^editrecordfromJTable/', views.editrecordfromJTable, name='editrecordfromJTable'),
    url(r'^deleterecordfromJTable/', views.deleterecordfromJTable, name='deleterecordfromJTable'),
    url(r'^getJoblistfromJTable/([0-9]+)?/$', views.getJoblistfromJTable, name='getJoblistfromJTable'),
    url(r'^addJobfromJTable/', views.addJobfromJTable, name='addJobfromJTable'),
    url(r'^editJobfromJTable/', views.editJobfromJTable, name='editJobfromJTable'),
    url(r'^deleteJobfromJTable/', views.deleteJobfromJTable, name='deleteJobfromJTable'),
    url(r'^changeswitchstate/', views.changeswitchstate, name='changeswitchstate'),
    url(r'^mobile/', views.mobile, name='mobile'),
    url(r'^jobs/', views.jobs, name='jobs'),



    url(r'^test/', views.test, name='test'),
    # url(r'^images/(?P<path>.*)$', 'django.views.static.serve',{'document_root' : '/Users/igor/PycharmProjects/RaspPiHome/images'}),
    # url(r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root' : '/Users/igor/PycharmProjects/RaspPiHome/css'}),
    # url(r'^jtable/(?P<path>.*)$', 'django.views.static.serve',{'document_root' : '/Users/igor/PycharmProjects/RaspPiHome/jtable'}),

    url(r'^admin/', admin.site.urls),

]
