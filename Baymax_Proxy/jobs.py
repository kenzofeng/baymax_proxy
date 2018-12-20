import logging
from datetime import datetime

import requests
from requests.exceptions import ConnectTimeout
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from proxy.models import Node
from robot_engine import utility

scheduler = BackgroundScheduler(executors={'default': ThreadPoolExecutor(40)})

scheduler.start()
logger = logging.getLogger('django')


@scheduler.scheduled_job('date', run_date=datetime.now())
@scheduler.scheduled_job('interval', minutes=5)
def sync_server():
    nodes = Node.objects.all().exclude(status='Running')
    for node in nodes:
        public_ip, private_ip = utility.getip(node.aws_instance_id)
        try:
            if public_ip:
                requests.get('http://{}:{}/status'.format(public_ip, node.port), timeout=10)
                node.status = "Done"
            else:
                node.status = "Error"
        except ConnectTimeout:
            node.status = "Error"
        except Exception as e:
            node.status = "Error"
            logger.error('Sync server error:{},ip:{},name:{}'.format(e, public_ip, node.name))
        node.host = public_ip
        node.save()
