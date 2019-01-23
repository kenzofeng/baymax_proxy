import logging
import os
from concurrent.futures import wait

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from proxy.models import Node
from robot_engine.pool import pool

logger = logging.getLogger('django')
scheduler = None
if os.environ.get("scheduler_lock") == "1":
    scheduler = BackgroundScheduler()
    scheduler.start()
    os.environ["scheduler_lock"] = os.environ.get("scheduler_lock") + "1"
    logger.info('scheduler started')


def check_node(node):
    if settings.HOST.lower() == 'private':
        node.host = node.private_ip
    elif settings.HOST.lower() == 'public':
        node.host = node.public_ip
    try:
        requests.get('http://{}:{}/status'.format(node.host, node.port), timeout=2)
        node.status = "Done"
    except Exception as e:
        node.status = "Error"
        logger.info('Sync server error:{},ip:{},name:{}'.format(e, node.host, node.name))
    node.save()


@scheduler.scheduled_job('interval', minutes=5)
def sync_server():
    nodes = Node.objects.all().exclude(status='Running')
    tasks = [pool.submit(check_node, node) for node in nodes]
    wait(tasks)
