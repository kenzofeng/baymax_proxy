import os
import subprocess
import logging
import svn.local
import svn.remote
import autobuild
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
        job_test.app = m.app
        job_test.save()
        result = Job_Test_Result()
        result.job_test = job_test
        result.log_path = "%s/Test_%s_%s.log" % (utility.gettoday(), m.test, utility.getnow())
        result.report = "%s/%s_%s" % (utility.gettoday(), utility.getnow(), m.test)
        utility.newlogger(job_test.name, result.log_path)
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
            if test.robot_parameter != "":
                testparameter.create_argfile_parameter(testpath, test.robot_parameter)
            else:
                testparameter.create_argfile(testpath, ts_case)
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


def run_autobuild(test, **parameter):
    oldpath = os.getcwd()
    status = False
    try:
        autobuild.logname = test.name
        test_app_autobuid = os.path.join(env.test, test.name, 'app', 'config.ini')
        test_app_autobuild_autobuid = os.path.join(env.test, test.name, 'app', 'autobuild', 'config.ini')
        if os.path.exists(test_app_autobuid, ):
            sha, branch = autobuild.build(test_app_autobuid, **parameter)
            status = True
        elif os.path.exists(test_app_autobuild_autobuid):
            sha, branch = autobuild.build(test_app_autobuild_autobuid, **parameter)
            status = True
        else:
            utility.job_test_log(test.name, "Can't found autobuild config.ini to build your app")
            return True
        test.project_sha = sha
        test.project_branch = branch
        test.save()
        return status
    except Exception, e:
        raise Exception("Autobuild Error:%s" % e)
    finally:
        os.chdir(oldpath)


def checkout_script(test):
    try:
        utility.job_test_log(test.name, "checkout test automation from svn")
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
