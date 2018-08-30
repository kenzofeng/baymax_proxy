import json
import os
import zlib

from serializers import ProjectSerializer, JobSerializer
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import env
from handler import job as job_handler
from models import Project, Job, Job_Test_Result, Job_Test, Node, Test_Map
import requests
from Baymax_Proxy.jobs import scheduler
import datetime


def job_start(request, project):
    myrequest = job_handler.Myrequest(request)
    scheduler.add_job(job_handler.start, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=1),
                      args=[myrequest, project])
    # rs = job_handler.start(myrequest, project)
    return JsonResponse({"status": "Job added successfully"}, safe=False)


def job_rerun(request, jobpk):
    myrequest = job_handler.Myrequest(request)
    scheduler.add_job(job_handler.rerun, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=1),
                      args=[myrequest, jobpk])
    # rs = job_handler.rerun(myrequest, jobpk)
    return JsonResponse({"status": "Job added successfully"}, safe=False)


def job_stop(request, project):
    rs = job_handler.stop(project)
    return JsonResponse({"status": rs}, safe=False)


def project_getall(request):
    list_project = Project.objects.all()
    list_project = [project.pk for project in list_project]
    return JsonResponse(list_project, safe=False)


def project_getallnodes(request):
    nodes = Node.objects.all()
    nodelist = [node.name for node in nodes]
    return JsonResponse(nodelist, safe=False)


def project_getdetail(request):
    tid = request.GET['tid']
    p = Project.objects.get(pk=tid)
    return JsonResponse(ProjectSerializer(p).data, safe=False)


@csrf_exempt
def project_save(request):
    p = json.loads(request.body)
    project = Project.objects.get(pk=p['pk'])
    serializer = ProjectSerializer(project, data=p)
    serializer.is_valid()
    serializer.save()
    return JsonResponse({'status': 'scuess'}, safe=False)


@csrf_exempt
def project_add(request):
    name = request.body
    if name != "":
        p = Project()
        p.name = name
        p.save()
    return JsonResponse({'status': 'scuess'}, safe=False)


@csrf_exempt
def project_delete(request):
    p = request.body
    project = Project.objects.get(pk=p)
    maps = Test_Map.objects.filter(project=project.pk)
    for m in maps:
        m.delete()
    project.node_set.clear()
    project.delete()
    return JsonResponse({'status': 'scuess'}, safe=False)


def job_project(request, project):
    return render(request, 'proxy/job_project.html', {"project": project})


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


def job_getall(request):
    number = request.GET['number']
    if 'project' in request.GET:
        project = request.GET['project']
        jobs = Job.objects.filter(project=project).order_by('-pk')[:number]
    else:
        jobs = Job.objects.all().order_by('-pk')[:number]
    job_s = JobSerializer.setup_eager_loading(jobs)
    return JsonResponse(JobSerializer(job_s, many=True, read_only=True).data, safe=False)


def lab_getall(request):
    p = Project.objects.all()
    ps = ProjectSerializer.setup_eager_loading(p)
    return JsonResponse(ProjectSerializer(ps, many=True, read_only=True).data, safe=False)
