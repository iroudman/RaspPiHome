from django.shortcuts import render, render_to_response,redirect
from pihome.models import devices,cronjobs
from forms import *
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import shutil
from datetime import datetime
import subprocess
from django.core.paginator import Paginator
from django.conf import settings
import datetime



@login_required(login_url='/login/')
def home(request):
    # if not request.user.is_authenticated():
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    devs = devices.objects.all()
    print "PILIGHT_CONFIG_FILE: %s" % settings.PILIGHT_CONFIG_FILE
    print "PILIGHT_START_COMMAND: %s" % settings.PILIGHT_START_COMMAND
    print "PILIGHT_STOP_COMMAND: %s" % settings.PILIGHT_STOP_COMMAND

    return render(request, 'index.html',{'devs': devs})




def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('login.html', context_instance=RequestContext(request))





@login_required(login_url='/login/')
def getdatatoedit(request):
    if request.POST.has_key('deviceid'):
        deviceid=request.POST['deviceid']
        dev = devices.objects.get(id=deviceid)
        print dev.name
        response = {'vname':dev.name,'vdesc':dev.description, 'vsystemcode':dev.systemcode, 'vdevicecode': dev.devicecode}

#        return HttpResponse(json.dumps(response),content_type='application/javascript')
        return JsonResponse(response)






@login_required(login_url='/login/')
def writeconfig(request):
    directory="/Users/igor/PycharmProjects/RaspPiHome/etc"

    tempfilename="/Users/igor/PycharmProjects/RaspPiHome/etc/config.json-NEW"

    srcfilename=os.path.join(directory,'config.json')
    dstfilename=os.path.join(directory,'config.json-%s' % datetime.now())


    shutil.copy(srcfilename, tempfilename)


    #stop Pilight service (to be implemented under Linux)
    #subprocess.call('ls')
    #generate JSON
    #load default config
    with open(srcfilename) as data_file:
         data = json.load(data_file)

#    data['devices']['testdev']['id'][0]['unitcode']=7
    devs = devices.objects.all()
    i=1
    for dev in devs:
        settingsdict={}
        protocollist=[]
        idlist=[]
        iddict={}
        protocollist.append('mumbi')

        systemcode = dev.systemcode
        devicecode = dev.devicecode


        #reverce the string
        systemcode = systemcode[::-1]
        devicecode = devicecode[::-1]




        iddict['systemcode']=int(systemcode, 2)
        iddict['unitcode']=int(devicecode, 2)

        idlist.append(iddict)
        settingsdict['protocol']=protocollist
        settingsdict['id']=idlist
        settingsdict['state']='off'
        data['devices'][dev.name]=settingsdict

    del data['devices']['testdev']


    with open(tempfilename, 'w') as outfile:
        json.dump(data,outfile,indent=4)


    #start Pilight service (to be implemented under Linux)

    return HttpResponseRedirect('/config')


@login_required(login_url='/login/')
def edit(request):
    devs = devices.objects.all()
    add_form = CreateAddForm()
    edit_form = CreateAddForm()
    response = {'devs':devs,'add_form':add_form, 'edit_form':edit_form}
    return render_to_response('edit.html',response,context_instance=RequestContext(request))

@login_required(login_url='/login/')
def addrecord(request):
    if request.method == 'POST':
        form = CreateAddForm(request.POST, request.FILES)

        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('/edit')
    return HttpResponseBadRequest("Error")

@login_required(login_url='/login/')
def editrecord(request):
    if request.method == 'POST':
        dev = devices.objects.get(id=request.POST.get('recordid'))
        form = CreateAddForm(request.POST, request.FILES, instance=dev)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('/edit')
    return HttpResponseBadRequest("Error")


@login_required(login_url='/login/')
def deleterecord(request, recordid):
    dev = devices.objects.get(id=recordid)
    dev.delete()
    return redirect('/edit')

@login_required(login_url='/login/')
def verify(request):
    filename="/Users/igor/PycharmProjects/RaspPiHome/etc/config.json"
    with open(filename) as data_file:
         data = json.load(data_file)
    return HttpResponse(json.dumps(data, indent=4), content_type="application/json")


@login_required(login_url='/login/')
def config(request):
    #PATH has to be changed
    directory="/Users/igor/PycharmProjects/RaspPiHome/etc"
    filenames = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.startswith('config'):
                filenames.append(filename)

    return render(request,"verify.html",{'filenames': filenames})

def test(request):
    devs = devices.objects.all()
    return render(request, 'test.html',{'devs': devs})

@login_required(login_url='/login/')
@csrf_exempt
def getlistfromJTable(request):
    jtStartIndex=request.GET.get('jtStartIndex')
    jtPageSize=request.GET.get('jtPageSize')
    jtSorting=request.GET.get('jtSorting')

    response_data = {}
    records = []

    response_data['Result'] = 'OK'
    allrecords = devices.objects.values('id','name','description','systemcode','devicecode')
    response_data['TotalRecordCount']=allrecords.count()
    p = Paginator(allrecords, jtPageSize)

    pagenumber=int(jtStartIndex)/int(jtPageSize)+1
    recordsinpage=p.page(pagenumber).object_list

    # for rec in recordsinpage:
    #     records.append(rec)

    records=list(recordsinpage)

    response_data['Records'] = records
    return JsonResponse(response_data, safe=False)


@login_required(login_url='/login/')
@csrf_exempt
def addrecordfromJTable(request):
    response_data = {}
    records={}

    if request.method == 'POST':
        form = CreateAddForm(request.POST, request.FILES)

        if form.is_valid():
            device = form.save(commit=False)
            device.save()

            records['name'] = device.name
            records['description'] = device.description
            records['systemcode'] = device.systemcode
            records['devicecode'] = device.devicecode
            records['id'] = device.id

            response_data['Result'] = 'OK'
            response_data['Record'] = records
            return JsonResponse(response_data)

    response_data['Result'] = 'Error'
    response_data['Message'] = "Data not valid"
    return JsonResponse(response_data)

@login_required(login_url='/login/')
@csrf_exempt
def editrecordfromJTable(request):
    response_data = {}
    records={}

    if request.method == 'POST':
        dev = devices.objects.get(id=request.POST.get('id'))
        form = CreateAddForm(request.POST, request.FILES, instance=dev)

        if form.is_valid():
            device = form.save(commit=False)
            device.save()
            response_data['Result'] = 'OK'
            return JsonResponse(response_data)

    response_data['Result'] = 'Error'
    response_data['Message'] = "Data not valid"
    return JsonResponse(response_data)


@login_required(login_url='/login/')
@csrf_exempt
def deleterecordfromJTable(request):
    response_data = {}

    if request.method == 'POST':
        dev = devices.objects.get(id=request.POST.get('id'))
        dev.delete()
        response_data['Result'] = 'OK'
        return JsonResponse(response_data)

    response_data['Result'] = 'Error'
    response_data['Message'] = "Data not valid"
    return JsonResponse(response_data)







@login_required(login_url='/login/')
@csrf_exempt
def getJoblistfromJTable(request, devid):
    jobs = cronjobs.objects.filter(deviceid=devid)
    response_data = {}
    records = []

    response_data['Result'] = 'OK'
    allrecords = jobs.values('id','deviceid','jobdescription','whattodo','startdate','starttime','enddate','endtime','periodicity')
    records=list(allrecords)
    response_data['Records'] = records
    return JsonResponse(response_data, safe=False)


@login_required(login_url='/login/')
@csrf_exempt
def addJobfromJTable(request):
    response_data = {}
    records={}

    if request.method == 'POST':
        print request.POST.get

        form = CreateAddJobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.save()


            records['deviceid'] = request.POST.get('deviceid')
            records['id'] = job.id
            records['jobdescription'] = job.jobdescription
            records['whattodo'] = job.whattodo
            records['startdate'] = job.startdate
            records['starttime'] = job.starttime
            records['enddate'] = job.enddate
            records['endtime'] = job.endtime
            records['periodicity'] = job.periodicity

            response_data['Result'] = 'OK'
            response_data['Record'] = records
            return JsonResponse(response_data)

    response_data['Result'] = 'Error'
    response_data['Message'] = "Data not valid"
    return JsonResponse(response_data)


@login_required(login_url='/login/')
@csrf_exempt
def editJobfromJTable(request):
    response_data = {}

    if request.method == 'POST':
        cronjob = cronjobs.objects.get(id=request.POST.get('id'))
        form = CreateAddJobForm(request.POST,instance=cronjob)

        if form.is_valid():
            job = form.save(commit=False)
            job.save()

            response_data['Result'] = 'OK'
            return JsonResponse(response_data)

    response_data['Result'] = 'Error'
    response_data['Message'] = "Data not valid"
    return JsonResponse(response_data)


@login_required(login_url='/login/')
@csrf_exempt
def deleteJobfromJTable(request):
    response_data = {}

    if request.method == 'POST':
        job = cronjobs.objects.get(id=request.POST.get('id'))
        job.delete()
        response_data['Result'] = 'OK'
        return JsonResponse(response_data)

    response_data['Result'] = 'Error'
    response_data['Message'] = "Data not valid"
    return JsonResponse(response_data)


@login_required(login_url='/login/')
def changeswitchstate(request):
    if request.POST.has_key('deviceid'):
        deviceid=request.POST['deviceid']
        dev = devices.objects.get(id=deviceid)
        systemcode = dev.systemcode
        devicecode = dev.devicecode

        #reverce the string
        systemcode = systemcode[::-1]
        devicecode = devicecode[::-1]


        if dev.status == True:
            #Switch Off
            print(settings.PILIGHT_SWITCH_OFF_COMMAND.format(int(systemcode, 2), int(devicecode, 2)))
#            subprocess.call(settings.PILIGHT_SWITCH_OFF_COMMAND.format(int(systemcode, 2), int(devicecode, 2)),shell=True)
            dev.status=False
            DeviceStatus = 'off'
        else:
            #Switch On
            print(settings.PILIGHT_SWITCH_ON_COMMAND.format(int(systemcode, 2), int(devicecode, 2)))
#            subprocess.call(settings.PILIGHT_SWITCH_ON_COMMAND.format(int(systemcode, 2), int(devicecode, 2)),shell=True)
            dev.status=True
            DeviceStatus = 'on'
        dev.save()

        response = {'status':DeviceStatus}
        return JsonResponse(response)

@login_required(login_url='/login/')
def mobile(request):
    devs = devices.objects.all()
    return render(request, 'mobile.html',{'devs': devs})


@login_required(login_url='/login/')
def jobs(request):
    jobs =  cronjobs.objects.all()
    cronjobslines = []
    for job in jobs:
        #job.deviceid is the device object. Not the ID
        command = getcommand(job.deviceid,job.whattodo)
        timesettings=getdatumzeit(job.startdate, job.starttime)
        cronjobline =""
        if job.periodicity == "once":
            cronjobline = "{0} {1} {2} {3} {4} {5}".format(timesettings['minute']
                                                           ,timesettings['hour']
                                                           ,timesettings['day']
                                                           ,timesettings['month']
                                                           ,'*'
                                                           ,command)
        elif job.periodicity == "daily":
            cronjobline = "{0} {1} {2} {3} {4} {5}".format(timesettings['minute']
                                                           ,timesettings['hour']
                                                           ,'*'
                                                           ,'*'
                                                           ,'*'
                                                           ,command)
        elif job.periodicity == "weekly":
            cronjobline = "{0} {1} {2} {3} {4} {5}".format(timesettings['minute']
                                                           ,timesettings['hour']
                                                           ,'*'
                                                           ,'*'
                                                           ,timesettings['weekday']
                                                           ,command)
        elif job.periodicity == "monthly":
            cronjobline = "{0} {1} {2} {3} {4} {5}".format(timesettings['minute']
                                                           ,timesettings['hour']
                                                           ,timesettings['day']
                                                           ,'*'
                                                           ,'*'
                                                           ,command)
        elif job.periodicity == "yearly":
            cronjobline = "{0} {1} {2} {3} {4} {5}".format(timesettings['minute']
                                                           ,timesettings['hour']
                                                           ,timesettings['day']
                                                           ,timesettings['month']
                                                           ,'*'
                                                           ,command)
        cronjobslines.append(cronjobline)
    return render(request, 'jobs.html',{'cronjobslines': cronjobslines})


def getdatumzeit(datum, zeit):
    datetimedict = {}
    datetimedict["year"] = datum.year
    datetimedict["month"] = datum.month
    datetimedict["day"] = datum.day
    datetimedict["weekday"] = datum.weekday()+1

    datetimedict["hour"] = zeit.hour
    datetimedict["minute"] = zeit.minute
    return datetimedict


def getcommand(dev, action):
    print dev

    systemcode = dev.systemcode
    devicecode = dev.devicecode

    #reverce the string
    systemcode = systemcode[::-1]
    devicecode = devicecode[::-1]
    if action == 'ON':
        return settings.PILIGHT_SWITCH_ON_COMMAND.format(int(systemcode, 2), int(devicecode, 2))
    else:
        return settings.PILIGHT_SWITCH_OFF_COMMAND.format(int(systemcode, 2), int(devicecode, 2))



