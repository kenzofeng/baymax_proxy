import json
import os

from django.core.exceptions import ObjectDoesNotExist

from proxy import env
from proxy.models import Job, Project, Job_Log, Test_Map, Job_Test, Job_Test_Result
from robot_engine import utility
from robot_engine.execute import Execute


class Myrequest:
    def __init__(self, request):
        self.host = request.get_host()
        self.GET = request.GET
        self.job_test_set = None
        self.set_data(request)

    def set_data(self, request):
        if request.body:
            data = json.loads(request.body)
            self.job_test_set = data['job_test_set']
        for test in self.job_test_set:
            setattr(self, test['name'], {'robot_parameter': test['robot_parameter']})


def stop(project):
    rs = []
    try:
        p = Project.objects.get(name=project)
        nodes = p.node_set.all()
        for node in nodes:
            ip = node.host
            rs.append(utility.stop_job(ip))
        return rs
    except Exception as e:
        raise Exception(e)


def init_job(project):
    p = Project.objects.get(pk=project)
    job = Job(project=project, status='Waiting', start_time=utility.gettime(),
              job_number="", email=p.email, servers=":".join([n.name for n in p.node_set.all()]))
    job.save()
    log = Job_Log()
    log.job = job
    log.path = "%s/project_%s_%s.log" % (utility.gettoday(), p.name, utility.getnow())
    log.save()
    utility.logmsg(log.path, "")
    return job


def copy_job(job_pk):
    job = Job.objects.get(pk=job_pk)
    job.pk = None
    job.save()
    job.status = 'Waiting'
    job.start_time = utility.gettime()
    job.end_time = None
    job.comments = ""
    job.save()
    log = Job_Log()
    log.job = job
    log.path = "%s/project_%s_%s.log" % (utility.gettoday(), job.project, utility.getnow())
    log.save()
    utility.logmsg(log.path, "")
    return job


def copy_job_test(request, job, jobpk):
    oldjob = Job.objects.get(pk=jobpk)
    old_job_test_set = oldjob.job_test_set.all()
    for m in old_job_test_set:
        job_test = Job_Test()
        job_test.job = job
        job_test.status = 'Waiting'
        job_test.robot_parameter = getattr(request, m.name)['robot_parameter']
        job_test.testurl = m.testurl
        job_test.name = m.name
        job_test.app = m.app
        job_test.save()
        result = Job_Test_Result()
        result.job_test = job_test
        result.log_path = "%s/Test_%s_%s.log" % (utility.gettoday(), m.name, utility.getnow())
        result.report = "%s/%s_%s" % (utility.gettoday(), utility.getnow(), m.name)
        utility.newlogger(job_test.name, result.log_path)
        result.save()


def init_jot_test(job):
    maps = Test_Map.objects.filter(project=job.project, use=True)
    if len(maps) == 0:
        raise Exception("please config test automation for project(%s)" % job.project)
    utility.mkdir(os.path.join(env.report, utility.gettoday()))
    for m in maps:
        job_test = Job_Test()
        job_test.job = job
        job_test.status = 'Waiting'
        job_test.robot_parameter = m.robot_parameter
        job_test.testurl = m.testurl
        job_test.name = m.test
        job_test.app = m.app
        job_test.save()
        result = Job_Test_Result()
        result.job_test = job_test
        result.log_path = "%s/Test_%s_%s.log" % (utility.gettoday(), m.test, utility.getnow())
        result.report = "%s/%s_%s" % (utility.gettoday(), utility.getnow(), m.test)
        utility.newlogger(job_test.name, result.log_path)
        result.save()


def start(request, project):
    try:
        utility.mkdir(os.path.join(env.log, utility.gettoday()))
        job = init_job(project)
        init_jot_test(job)
        execute = Execute(job, request.host, request)
        execute.run()
        job.status = 'Done'
        job.end_time = utility.gettime()
        job.save()
        utility.save_log(job)
        return get_results(request, job)
    except ObjectDoesNotExist:
        raise Exception("%s doesn't exist,please config in Baymax System!" % (project))
    except Exception as e:
        job.end_time = utility.gettime()
        job.status = 'Error'
        job.save()
        utility.logmsg(job.job_log.path, str(e))
        utility.save_log(job)
        raise Exception("start job error:{}".format(e))


def rerun(request, jobpk):
    try:
        utility.mkdir(os.path.join(env.log, utility.gettoday()))
        job = copy_job(jobpk)
        copy_job_test(request, job, jobpk)
        execute = Execute(job, request.host, request)
        execute.run()
        job.status = 'Done'
        job.end_time = utility.gettime()
        job.save()
        utility.save_log(job)
        return get_results(request, job)
    except Exception as e:
        job.end_time = utility.gettime()
        job.status = 'Error'
        job.save()
        utility.logmsg(job.job_log.path, str(e))
        utility.save_log(job)
        raise Exception("rerun job error:{}".format(e))


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
