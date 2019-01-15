import logging
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from requests.exceptions import ConnectTimeout

from proxy.models import Node
from robot_engine import utility

logger = logging.getLogger('django')
scheduler = None
if os.environ.get("scheduler_lock") == "1":
    scheduler = BackgroundScheduler()
    scheduler.start()
    os.environ["scheduler_lock"] = os.environ.get("scheduler_lock") + "1"
    logger.info('scheduler started')


@scheduler.scheduled_job('interval', minutes=5)
def sync_server():
    nodes = Node.objects.all().exclude(status='Running')
    for node in nodes:
        # public_ip, private_ip = utility.getip(node.aws_instance_id)
        if settings.HOST.lower() == 'private':
            node.host = node.private_ip
        elif settings.HOST.lower() == 'public':
            node.host = node.public_ip
        try:
            requests.get('http://{}:{}/status'.format(node.host, node.port), timeout=2)
            node.status = "Done"
        except ConnectTimeout:
            node.status = "Error"
        except Exception as e:
            node.status = "Error"
            logger.error('Sync server error:{},ip:{},name:{}'.format(e, node.host, node.name))
        node.save()
