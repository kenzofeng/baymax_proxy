import requests
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import wait

pool = ThreadPoolExecutor(max_workers=10)


def checkstatus(host, port):
    try:
        requests.get('http://{}:{}/status'.format(host, port), timeout=10)
        return host,True
    except Exception:
        return host,False


class node:
    def __init__(self, host, port):
        self.host = host
        self.port = port


nodes = [node('34.215.169.80', '51234')]

tasks = [pool.submit(checkstatus, n.host, n.port) for n in nodes]
wait(tasks)
for t in tasks:
    h, s = t.result()
    if s:
        print(h)
