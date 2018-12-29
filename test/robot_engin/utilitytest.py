from collections import namedtuple

from django.test import TestCase

from proxy.models import Job
from robot_engine.utility import zipreport, send_email
from datetime import datetime


class UiltiTest(TestCase):
    def setUp(self):
        self.j = Job.objects.create(project="ShopStorage", email='daniel.liu@derbysoft.com', start_time=datetime.now())

    def test_send_email(self):
        job_test_result = namedtuple('job_test_result', ['id'])

        jts = job_test_result('1')

        job = namedtuple('job',
                         ['email', 'start_time', 'project', 'project_version', 'id'])

        jj = job('daniel.liu@derbysoft.com', self.j.start_time, 'ShopStorage',
                 '/usr/local/applications/shop-storage-dswitch/git.properties git.branch= git.commit.id=5a91b4b5ec504d48fc1552f1140c2bff35b7efc7 /usr/local/applications/shop-storage-save-ari/git.properties git.branch= git.commit.id=5a91b4b5ec504d48fc1552f1140c2bff35b7efc7',
                 '1')

        Test = namedtuple('Test', ['job', 'job_test_result', 'name', 'id', 'status', 'revision_number'])
        test = Test(jj, jts, 'shop-storage-daily', '1', 'PASS', "15716")

        send_email(test, 'http://baymax.com/')

    # def test_zip_report(self):
    #     zipreport((('it-bw-exp-ari', '/home/feng/derbysoftsvn/it-bw-exp-ari')))
