# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from django.core import serializers
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from handler import job as job_handler
from handler import project as project_handler
from models import Project, Job


def job_start(request, project):
    rs = job_handler.start(request, project)
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
    list_job = Job.objects.all().order_by('-pk')[:number]
    results = []
    for job in list_job:
        tests = []
        start_time = ""
        end_time = ''
        if job.start_time is not None:
            start_time = job.start_time.strftime('%Y-%m-%d %H:%M:%S')
        if job.end_time is not None:
            end_time = job.end_time.strftime('%Y-%m-%d %H:%M:%S')
        myjob = {'name': job.project, 'status': job.status, 'start': start_time,
                 'end': end_time, 'tests': tests}
        for test in job.job_test_set.all():
            tests.append(
                {'name': test.name, 'parameter': test.robot_parameter, 'status': test.status,
                 'log': test.job_test_result.id,
                 'id': test.id})
        if not tests:
            continue
        results.append(myjob)
    return HttpResponse(json.dumps(results), content_type='application/json')


def lab(request):
    return render(request, 'proxy/lab.html')


def lab_getall(request):
    json_rs = project_handler.get_all()
    return HttpResponse(json_rs, content_type='application/json')
