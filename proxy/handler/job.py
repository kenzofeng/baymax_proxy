import json
import os

from django.core.exceptions import ObjectDoesNotExist

from proxy import env
from proxy.models import Job, Project, Job_Log
from robot_engine import utility
from robot_engine.execute import Execute


class Myrequest:
    def __init__(self, request):
        self.host = request.get_host()
        self.GET = request.GET


def start(request, project):
    try:
        p = Project.objects.get(pk=project)
        utility.mkdir(os.path.join(env.log, utility.gettoday()))
        job = Job(project=project, status='waiting', start_time=utility.gettime(),
                  job_number="", email=p.email)
        job.save()
        log = Job_Log()
        log.job = job
        log.path = "%s/project_%s_%s.log" % (utility.gettoday(), p.name, utility.getnow())
        log.save()
        utility.logmsg(log.path, "")
        execute = Execute(job, request.host, request)
        execute.run()
        job.status = 'Done'
        job.end_time = utility.gettime()
        job.save()
        utility.save_log(job)
        return get_results(request, job)
    except ObjectDoesNotExist:
        raise Exception("%s doesn't exist,please config in Baymax System!" % (project))
    except Exception, e:
        job.end_time = utility.gettime()
        job.status = 'Error'
        job.save()
        utility.logmsg(job.job_log.path, str(e))
        utility.save_log(job)
        raise Exception(e)


def get_results(request, job):
    jtests = job.job_test_set.all()
    status = True
    result = {}
    tests = []
    for t in jtests:
        testdict = {}
        status = t.status
        testdict['name'] = t.name
        testdict['status'] = t.status
        testdict['report'] = "http://%s/regression/report/%s" % (request.host, t.id)
        testdict['runtime_log'] = "http://%s/regression/test/log/%s" % (request.host, t.job_test_result.id)
        tests.append(testdict)
        if status == 'FAIL':
            status = False
    if status:
        result['result'] = 'PASS'
    else:
        result['result'] = 'FAIL'
    result['tests'] = tests
    return json.dumps(result)
