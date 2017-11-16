# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import utility
from proxy.models import Test_Map, Job_Test, Job_Test_Result


def jot_test_init(job):
    maps = Test_Map.objects.filter(project=job.project, use=True)
    if len(maps) == 0:
        raise Exception("please config test automation for project(%s)" % job.project)
    for m in maps:
        job_test = Job_Test()
        job_test.job = job
        job_test.status = 'Waiting'
        job_test.robot_parameter = m.robot_parameter
        job_test.testurl = m.testurl
        job_test.name = m.test
        job_test.save()
        result = Job_Test_Result()
        result.test = job_test
        result.log_path = "%s/Test_%s_%s.log" % (utility.gettoday(), m.test, utility.getnow())
        result.report = "%s/%s_%s" % (utility.gettoday(), utility.getnow(), m.test)
        result.save()
