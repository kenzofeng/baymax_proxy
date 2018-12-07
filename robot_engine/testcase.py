import os

import svn.local
import svn.remote

from proxy import env
from proxy.models import Job_Test_Distributed_Result
from . import testparameter, utility
from .testrun import TestRun


def distribute_test_script(nodes, test):
    testpath = os.path.join(env.test, test.name)
    testrun = TestRun(len(nodes), testpath, test.robot_parameter)
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
    except UnicodeDecodeError:
        pass
    except Exception as e:
        raise Exception("Checkout Automation Script Error:%s" % e)
    try:
        l = svn.local.LocalClient(testpath)
        test.revision_number = l.info()['commit#revision']
        test.save()
    except Exception as e:
        raise Exception("Get Svn Vision Automation Script Error:%s" % e)
