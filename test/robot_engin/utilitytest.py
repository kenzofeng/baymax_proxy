from robot_engine.utility import cat_version, zipreport, send_email
from collections import namedtuple

# print(cat_version('54.184.212.50', '/usr/local/webapps/expedia-pusher/WEB-INF/classes/git.properties'))


# zipreport((('it-bw-exp-ari','/home/feng/derbysoftsvn/it-bw-exp-ari')))

job_test_result = namedtuple('job_test_result', ['id'])

jts = job_test_result('1')

Job = namedtuple('job',
                 ['email', 'start_time', 'project', 'project_version', 'id'])

job = Job('daniel.liu@derbysoft.com', '2018-12-29 05:46:05.891763+00:00', 'ShopStorage',
          '/usr/local/applications/shop-storage-dswitch/git.properties git.branch= git.commit.id=5a91b4b5ec504d48fc1552f1140c2bff35b7efc7 /usr/local/applications/shop-storage-save-ari/git.properties git.branch= git.commit.id=5a91b4b5ec504d48fc1552f1140c2bff35b7efc7',
          '1')

Test = namedtuple('Test',['job', 'job_test_result' ,'name', 'id', 'status', 'revision_number'])
test = Test(job,jts,'shop-storage-daily','1','PASS',"15716")

send_email(test, 'http://baymax.com/')
