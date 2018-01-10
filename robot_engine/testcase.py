import os
import subprocess

import svn.local
import svn.remote

import utility
from proxy import env
from proxy.models import Test_Map, Job_Test, Job_Test_Result, Job_Test_Distributed_Result
from testrun import TestRun
import testparameter


def jot_test_init(job):
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
        job_test.save()
        result = Job_Test_Result()
        result.job_test = job_test
        result.log_path = "%s/Test_%s_%s.log" % (utility.gettoday(), m.test, utility.getnow())
        result.report = "%s/%s_%s" % (utility.gettoday(), utility.getnow(), m.test)
        result.save()


def distribute_test_script(nodes, test):
    testpath = os.path.join(env.test, test.name)
    testrun = TestRun(len(nodes), testpath)
    for ts_case in testrun.RunCase:
        if len(ts_case) != 0:
            test_ds = Job_Test_Distributed_Result()
            test_ds.job_test = test
            test_ds.save()
            test_ds.script = "%s/%s_%s" % (utility.gettoday(), test.name, test_ds.pk)
            test_ds.report = "%s/report_%s_%s" % (utility.gettoday(), test.name, test_ds.pk)
            test_ds.save()
            utility.mkdir(os.path.join(env.tmp, utility.gettoday()))
            utility.mkdir(os.path.join(env.report, utility.gettoday()))
            testparameter.create_argfile(ts_case, testpath)
            utility.zip_file(testpath, os.path.join(env.tmp, "%s.zip" % test_ds.script))


def delete_distribute_test_script(test):
    testpath = os.path.join(env.test, test.name)
    for test_ds in test.job_test_distributed_result_set.all():
        utility.remove_file(os.path.join(env.tmp, "%s.zip" % test_ds.script))


def delete_distribute_test_report(test):
    test_ds_reports = [os.path.join(env.tmp, test_ds.report) for test_ds in
                       test.job_test_distributed_result_set.all() if
                       os.path.exists(os.path.join(env.tmp, test_ds.report))]
    for reprot in test_ds_reports:
        utility.remove_file("%s.zip" % reprot)
        utility.remove_file(reprot)

def run_autobuild(test, parameter):
    try:
        log = None
        opath = os.getcwd()
        status = False
        test_app_autobuid = os.path.join(env.test, test.name, 'app', 'autobuild.py')
        test_app_autobuild_autobuid = os.path.join(env.test, test.name, 'app', 'autobuild', 'autobuild.py')
        pid = 0
        if os.path.exists(test_app_autobuid):
            command = "python %s run" % (test_app_autobuid)
            utility.logmsg(test.job_test_result.log_path, command)
            os.chdir(os.path.join(env.test, test.name, 'app'))
            autobuild = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            pid = autobuild.pid
        elif os.path.exists(test_app_autobuild_autobuid):
            command = "python %s run" % (test_app_autobuild_autobuid)
            utility.logmsg(test.job_test_result.log_path, command)
            os.chdir(os.path.join(env.test, test.name, 'app', 'autobuild'))
            autobuild = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            pid = autobuild.pid
        else:
            utility.logmsg(test.job_test_result.log_path, "not found autobuild.py to build your app")
            os.chdir(opath)
            return True
        while True:
            log = autobuild.stdout.readline()
            utility.logmsgs(test.job_test_result.log_path, log.replace('\r\n', ''))
            if '|-ERROR' in log:
                status = False
                break
            if 'File is not exists' in log:
                status = False
                break
            if autobuild.poll() is not None:
                status = True
                break
        os.chdir(opath)
        utility.kill(pid)
        return status
    except Exception, e:
        raise Exception("Autobuild Error:%s" % e)


def checkout_script(test):
    try:
        utility.logmsg(test.job_test_result.log_path, "checkout test automation from svn")
        testpath = os.path.join(env.test, test.name)
        if os.path.exists(testpath):
            utility.remove_file(testpath)
            utility.remove_file(testpath)
            utility.remove_file(testpath)
        os.mkdir(testpath)
        r = svn.remote.RemoteClient(test.testurl)
        r.checkout(testpath)
        l = svn.local.LocalClient(testpath)
        test.revision_number = l.info()['commit#revision']
        test.save()
    except Exception, e:
        raise Exception("Checkout Automation Script Error:%s" % e)
