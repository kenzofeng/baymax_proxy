# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import time
from datetime import *

import manage
import testcase
import testparameter
import utility
from proxy import env
from proxy.models import Job, Node, Job_Test_Distributed_Result
from testrun import TestRun

mswindows = (sys.platform == "win32")


class Execute():
    def __init__(self, job, ip, parameter):
        self.ip = ip
        self.job = job
        self.parameter = parameter
        self.nodes = Node.objects.all()

    def run(self):
        testcase.jot_test_init(self.job)
        self.do_job()

    def do_job(self):
        preid = int(self.job.id) - 1
        while True:
            try:
                prejob = Job.objects.get(pk=preid)
                if prejob.status == 'Done' or prejob.status == 'Error':
                    break
            except Exception:
                break
            time.sleep(2)
        self.job.status = 'running'
        self.job.save()
        job_tests = self.job.job_test_set.all()
        for test in job_tests:
            self.execute(test)

    def distribute_test_script(self, test):
        testpath = os.path.join(env.test, test.name)
        testrun = TestRun(len(self.nodes), testpath)
        for ts_case in testrun.RunCase:
            test_ds_random_str = utility.random_str()
            test_ds = Job_Test_Distributed_Result()
            test_ds.job_test = test
            test_ds.script = "%s_%s" % (test.name, test_ds_random_str)
            test_ds.report = "%s/%s_%s" % (
                utility.gettoday(), datetime.utcnow().strftime('%H%M%S'), test.name, test_ds_random_str)
            test_ds.save()
            testparameter.create_argfile(ts_case, testpath)
            utility.zip_file(testpath, os.path.join(env.tmp, test_ds.script))

    def execute(self, test):
        try:
            test.status = 'running'
            test.save()
            manage.test_checkout(test)
            if utility.run_autobuild(test, self.parameter):
                self.distribute_test_script()
            else:
                pass
        except Exception, e:
            print e


            # def execute(self, test):
            #     try:
            #         robot = None
            #         opath = os.getcwd()
            #         test.status = 'running'
            #         test.save()
            #         manage.test_checkout(test)
            #         utility.update_Doraemon()
            #         if utility.run_autobuild(test):
            #             testpath = os.path.join(env.test, test.name)
            #             reportpath = os.path.join(env.report, test.report)
            #             os.chdir(testpath)
            #             if mswindows:
            #                 command = "pybot.bat  %s --outputdir %s  %s" % (test.robot_parameter, reportpath, testpath)
            #                 utility.logmsg(test.test_log.path, command)
            #                 robot = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            #             else:
            #                 command = "pybot  %s --outputdir %s  %s" % (test.robot_parameter, reportpath, testpath)
            #                 utility.logmsg(test.test_log.path, command)
            #                 robot = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            #             test.pid = robot.pid
            #             test.save()
            #             while True:
            #                 log = robot.stdout.readline()
            #                 utility.logmsgs(test.test_log.path, log.replace('\r\n', ''))
            #                 if robot.poll() is not None:
            #                     break
            #             test.status = utility.get_result_fromxml(os.path.join(reportpath, env.output_xml))
            #             test.save()
            #         else:
            #             test.status = 'error'
            #             test.save()
            #         utility.send_email(test, self.ip)
            #     except Exception, e:
            #         test.status = 'error'
            #         test.save()
            #         utility.send_email(test, self.ip)
            #         utility.logmsg(test.test_log.path, e)
            #     finally:
            #         utility.save_test_log(test)
            #         if robot is not None:
            #             robot.terminate()
            #         os.chdir(opath)
