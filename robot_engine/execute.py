import datetime
import logging
import os
import time
from concurrent.futures import wait

import requests

from Baymax_Proxy.jobs import scheduler
from proxy import env
from proxy.models import Project, Job
from . import testcase, testresult, utility
from .pool import pool

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
        job_tests = self.job.job_test_set.all()
        for test in job_tests:
            self.execute(test, status)

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
        except Exception as e:
            logger.error("test error:{}".format(e))
        finally:
            node.status = "Done"
            node.save()

    def send_test(self, test):
        request_tasks = []
        test_ds_all = test.job_test_distributed_result_set.all()
        for test_ds, node in zip(test_ds_all, self.nodes):
            node.status = 'Running'
            node.save()
            test_ds.host = "{}:{}".format(node.host, node.port)
            test_ds.save()
            # self.request_test(test_ds,node)
            request_tasks.append(pool.submit(self.request_test, test_ds, node))
            # rt = threading.Thread(target=self.request_test, args=(test_ds, node))
            # rt.setDaemon(True)
            # rt.start()
            # request_threads.append(rt)
        # for rq in request_threads:
        #     rq.join()
        wait(request_tasks)

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
        tasks = [pool.submit(self.requeststatus, node.host, node.port) for node in nodes]
        wait(tasks)
        for t in tasks:
            h, s = t.result()
            if s:
                for node in nodes:
                    if node.host == h:
                        newnodes.append(node)
                        break
        return newnodes

    def requeststatus(self, host, port):
        try:
            requests.get('http://{}:{}/status'.format(host, port), timeout=10)
            return host, True
        except Exception:
            return host, False

    def check_job_status(self, jobnodes):
        last_job = Job.objects.filter(servers=jobnodes).order_by('-pk')[:20]
        if len(last_job) > 1:
            for i, j in enumerate(last_job):
                if j.pk == self.job.pk:
                    if last_job[i + 1].status in ['Done', 'Error']:
                        return True
                    else:
                        return False
        else:
            return True

    def check_use_node_server(self):
        p = Project.objects.get(name=self.job.project)
        nodes = p.node_set.all()
        if len(nodes) == 0:
            raise Exception("There is no node server to use")
        jobnodes = ':'.join([node.name for node in nodes])
        while True:
            if self.check_job_status(jobnodes):
                break
            time.sleep(1)
        # self.updatenodes(nodes)
        self.nodes = self.checknodestatus(nodes)
        while True:
            p = Project.objects.get(name=self.job.project)
            nodes = p.node_set.all()
            status = any([node.status == 'Error' for node in nodes])
            if status:
                return False
            status = all([node.status == 'Done' for node in nodes])
            if status:
                break
            time.sleep(1)
        self.job.status = 'Running'
        self.job.save()
        return True

    def execute(self, test, status):
        try:
            if status:
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
                                  run_date=datetime.datetime.now() + datetime.timedelta(seconds=2),
                                  args=[test, self.ip])
            else:
                test.status = 'Error'
                test.save()
                raise Exception("Project Servers Status is Error")
        except Exception as e:
            logger.error("execute error:{}".format(e))
            test.status = 'Error'
            test.save()
            utility.job_test_log(test.name, e)
        finally:
            testcase.delete_distribute_test_report(test)
            testcase.delete_distribute_test_script(test)
            utility.save_test_log(test)
