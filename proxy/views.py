import json
import os
import zlib

from django.core import serializers
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import env
from handler import job as job_handler
from handler import project as project_handler
from models import Project, Job, Job_Test_Result, Job_Test
import requests
from Baymax_Proxy.jobs import scheduler
import datetime


def job_start(request, project):
    myrequest = job_handler.Myrequest(request)
    scheduler.add_job(job_handler.start, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=2),
                      args=[myrequest, project])
    return HttpResponse({"status": "true"}, content_type='application/json')


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


def test_run_log(request, logid):
    job_test_result = Job_Test_Result.objects.get(pk=logid)
    job_test = job_test_result.job_test
    log = job_test_result.log
    joblog = ''
    if log is not None:
        log = zlib.decompress(log.decode("base64"))
        for l in log.split('\n'):
            joblog = joblog + "<span>%s</span><br/>" % (l)
        return HttpResponse(joblog, content_type='text/html')
    else:
        try:
            logpath = os.path.join(env.log, job_test_result.log_path)
            if os.path.exists(logpath):
                f = open(logpath, 'r')
                fst = f.read()
                f.close()
                for l in fst.split('\n'):
                    joblog = joblog + "<span>%s</span><br/>" % (l)
            test_ds_all = job_test.job_test_distributed_result_set.all()
            for test_ds in test_ds_all:
                try:
                    r = requests.get("http://%s/test/log/%s" % (test_ds.host, test_ds.pk), timeout=5)
                    joblog = joblog + r.content
                except Exception, e:
                    joblog = joblog + str(e)
        except Exception, e:
            return HttpResponse(e)
    return HttpResponse(joblog, content_type='text/html')


def test_log(request, logid):
    result = ""
    test = Job_Test.objects.get(pk=logid)
    path = os.path.join(env.report, test.job_test_result.report, env.log_html)
    if os.path.exists(path):
        f = open(path)
        result = f.read()
        f.close()
    return HttpResponse(result, content_type='text/html')


def test_report(request, logid):
    test = Job_Test.objects.get(pk=logid)
    path = os.path.join(env.report, test.job_test_result.report, env.report_html)
    f = open(path)
    return HttpResponse(f.read(), content_type='text/html')


def test_cache(request, logid, cid):
    test = Job_Test.objects.get(pk=logid)
    path = os.path.join(env.report, test.job_test_result.report, 'cache', cid)
    f = open(path)
    return HttpResponse(f.read(), content_type='text')


def test_compare(request, logid, cid):
    test = Job_Test.objects.get(pk=logid)
    path = os.path.join(env.report, test.job_test_result.report, 'compare', cid)
    f = open(path)
    return HttpResponse(f.read(), content_type='text/html')


def test_redfile(request, logid, redfile):
    test = Job_Test.objects.get(pk=logid)
    path = os.path.join(env.report, test.job_test_result.report, 'compare', env.deps, redfile)
    f = open(path)
    return HttpResponse(f.read(), content_type='text/css')


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
                 'project_branch': test.project_branch, 'project_sha': test.project_sha,
                 'version': test.revision_number,
                 'log': test.job_test_result.id,
                 'id': test.id})
        if not tests:
            continue
        results.append(myjob)
    return HttpResponse(json.dumps(results), content_type='application/json')


@csrf_exempt
def job_search(request):
    list_job = Job.objects.filter(project=request.POST['pj[pk]']).order_by('-start_time')
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
                 'project_branch': test.project_branch, 'project_sha': test.project_sha,
                 'version': test.revision_number,
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
