from apscheduler.schedulers.background import BackgroundScheduler
from proxy.models import Node
from robot_engine import utility
import requests
from requests import ConnectionError
from datetime import datetime
import logging

scheduler = BackgroundScheduler()

scheduler.start()
logger = logging.getLogger('django')


@scheduler.scheduled_job('date', run_date=datetime.now())
@scheduler.scheduled_job('interval', minutes=5)
def sync_server():
    nodes = Node.objects.all()
    for node in nodes:
        public_ip, private_ip = utility.getip(node.aws_instance_id)
        try:
            if public_ip != "":
                requests.get('http://{}:{}/status'.format(public_ip, node.port), timeout=5)
                node.status = "Done"
            else:
                node.status = "Error"
        except ConnectionError:
            node.status = "Error"
        except Exception as e:
            logger.error('Sync server error:{},ip:{},name:{}'.format(e, public_ip, node.name))
        node.host = public_ip
        node.save()
