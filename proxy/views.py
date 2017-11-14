# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core import serializers
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import Project
from handler import project as project_handler


def job_start(request):
    rs = {'status':'sccuess'}
    return HttpResponse(json.dumps(rs), content_type='application/json')

def project(request):
    return render(request, 'proxy/project.html')


def project_getall(request):
    list_project = Project.objects.all()
    return HttpResponse(serializers.serialize("json", list_project), content_type='application/json')


def project_getdetail(request):
    tid = request.GET['tid']
    p = Project.objects.get(pk=tid)
    json_rs = project_handler.to_json(p)
    return HttpResponse(json_rs, content_type='application/json')


@csrf_exempt
def project_add(request):
    name = request.POST['name']
    if name != "":
        p = Project()
        p.name = name
        p.save()
    return HttpResponse(json.dumps({'status': 'scuess'}), content_type='application/json')


@csrf_exempt
def project_update(request):
    project_handler.update(request)
    return HttpResponse(json.dumps({'status': 'scuess'}), content_type='application/json')


@csrf_exempt
def project_delete(request):
    project_handler.delete(request)
    return HttpResponse(json.dumps({'status': 'scuess'}), content_type='application/json')


def job(request):
    return render(request, 'proxy/job.html')


def job_getall(request, number):
    return HttpResponse(json.dumps({}), content_type='application/json')


def lab(request):
    return render(request, 'proxy/lab.html')


def lab_getall(request):
    json_rs = project_handler.get_all()
    return HttpResponse(json_rs, content_type='application/json')
