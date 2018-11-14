import logging
import os
import sys
import threading
import time
import requests

import testcase
import testresult
import utility
from proxy import env
from proxy.models import Project
from Baymax_Proxy.jobs import scheduler
import datetime

logger = logging.getLogger('django')


class Execute():
    def __init__(self, job, ip, request):
        self.ip = ip
        self.job = job
        self.GET = request.GET
        self.nodes = None

    def run(self):
        self.do_job()

    def do_job(self):
        status = self.check_use_node_server()
        if status:
            job_tests = self.job.job_test_set.all()
            for test in job_tests:
                self.execute(test)

    def request_test(self, test_ds, node):
        try:
            r = requests.post(
                "http://{}:{}/{}/{}/start".format(node.host, node.port, test_ds.job_test.name, test_ds.pk),
                data={"filename": "%s_%s.zip" % (test_ds.job_test.name, test_ds.pk), "app": test_ds.job_test.app},
                files={
                    "script": open(os.path.join(env.tmp, "%s.zip" % test_ds.script), 'rb')})
            download_zip = os.path.join(env.tmp, utility.gettoday(), "report_%s.zip" % r.headers["filename"])
            open(download_zip, 'wb').write(r.content)
            utility.extract_zip(download_zip, os.path.join(env.tmp, test_ds.report))
        except Exception, e:
            logger.error("test error:{}".format(e))
        finally:
            node.status = "Done"
            node.save()

    def send_test(self, test):
        request_threads = []
        test_ds_all = test.job_test_distributed_result_set.all()
        for test_ds, node in zip(test_ds_all, self.nodes):
            node.status = 'Running'
            node.save()
            test_ds.host = "{}:{}".format(node.host, node.port)
            test_ds.save()
            # self.request_test(test_ds,node)
            rt = threading.Thread(target=self.request_test, args=(test_ds, node))
            rt.setDaemon(True)
            rt.start()
            request_threads.append(rt)
        for rq in request_threads:
            rq.join()

    def merge_test_report(self, test):
        test_report = os.path.join(env.report, test.job_test_result.report)
        test_ds_reports = [os.path.join(env.tmp, test_ds.report) for test_ds in
                           test.job_test_distributed_result_set.all() if
                           os.path.exists(os.path.join(env.tmp, test_ds.report))]
        for r in test_ds_reports:
            utility.copytree(r, test_report)
        test_ds_reports = tuple([os.path.join(ds_report, env.output_xml) for ds_report in test_ds_reports])
        testresult.merge_report(test_report, *test_ds_reports)

    def updatenodes(self, nodes):
        for node in nodes:
            instantce_id = node.aws_instance_id
            public_ip, private_ip = utility.getip(instantce_id)
            node.host = public_ip
            node.save()

    def checknodestatus(self, nodes):
        newnodes = []
        for node in nodes:
            try:
                requests.get('http://{}:{}/status'.format(node.host, node.port))
                newnodes.append(node)
            except Exception as e:
                pass
        return newnodes

    def check_use_node_server(self):
        p = Project.objects.get(name=self.job.project)
        nodes = p.node_set.all()
        if len(nodes) == 0:
            raise Exception("There is no node server to use")
        self.updatenodes(nodes)
        self.nodes = self.checknodestatus(nodes)
        while True:
            p = Project.objects.get(name=self.job.project)
            nodes = p.node_set.all()
            status = any([node.status == 'Error' for node in nodes])
            if status:
                logger.error("Test Node Status is Error")
                self.job.status = 'Error'
                self.job.save()
                raise Exception("All Servers Status is Error")
            status = all([node.status == 'Done' for node in nodes])
            if status:
                break
        self.job.status = 'Running'
        self.job.save()
        return True

    def execute(self, test):
        try:
            test.status = 'Running'
            test.save()
            testcase.checkout_script(test)
            testcase.distribute_test_script(self.nodes, test)
            self.send_test(test)
            self.merge_test_report(test)
            test.status = utility.get_result_fromxml(
                os.path.join(env.report, test.job_test_result.report, env.output_xml))
            test.save()
            scheduler.add_job(utility.send_email, 'date',
                              run_date=datetime.datetime.now() + datetime.timedelta(seconds=2), args=[test, self.ip])
        except Exception, e:
            logger.error("execute error:{}".format(e))
            test.status = 'Error'
            test.save()
            utility.job_test_log(test.name, e)
        finally:
            testcase.delete_distribute_test_report(test)
            testcase.delete_distribute_test_script(test)
            utility.save_test_log(test)
