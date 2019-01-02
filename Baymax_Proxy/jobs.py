import logging

from django.conf import settings
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import ConnectTimeout

from proxy.models import Node
from robot_engine import utility

scheduler = BackgroundScheduler()
scheduler.start()
logger = logging.getLogger('django')


@scheduler.scheduled_job('interval', minutes=5)
def sync_server():
    nodes = Node.objects.all().exclude(status='Running')
    for node in nodes:
        public_ip, private_ip = utility.getip(node.aws_instance_id)
        try:
            if public_ip:
                requests.get('http://{}:{}/status'.format(private_ip, node.port), timeout=10)
                node.status = "Done"
            else:
                node.status = "Error"
        except ConnectTimeout:
            node.status = "Error"
        except Exception as e:
            node.status = "Error"
            logger.error('Sync server error:{},ip:{},name:{}'.format(e, private_ip, node.name))
        if settings.HOST.lower() == 'private':
            node.host = private_ip
        elif settings.HOST.lower() == 'public':
            node.host = public_ip
        node.public_ip = public_ip
        node.private_ip = private_ip
        node.save()
