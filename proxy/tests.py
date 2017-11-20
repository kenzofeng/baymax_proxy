# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import shutil

import env
from django.test import TestCase
import requests
from robot_engine import utility

# # Create your tests here.
# r = requests.post("http://%s/%s/%s/start" % ("10.200.152.27.:8888", "channel_Tuniu_endpoint", "60"), data={"filename":"channel_Tuniu_endpoint_60.zip"},
#                   files={
#                       "script": open(r'D:\workspace\Baymax_Proxy\project\tmp\20171118\channel_Tuniu_endpoint_60.zip', 'rb')})
# print r
# utility.mkdir(os.path.join(env.tmp, '20171117','pixiu_1'))
# utility.zip_file(r'D:\workspace\Baymax_Proxy\project\test_automation\pixiu',r'D:\workspace\Baymax_Proxy\project\tmp\20171117\pixiu_1.zip')
# utility.mkdir(os.path.join(env.tmp, '20171117','pixiu_2'))
# utility.zip_file(r'D:\workspace\Baymax_Proxy\project\test_automation\pixiu',r'D:\workspace\Baymax_Proxy\project\tmp\20171117\pixiu_2.zip')
# utility.mkdir(os.path.join(env.tmp, '20171117','pixiu_3'))
# utility.zip_file(r'D:\workspace\Baymax_Proxy\project\test_automation\pixiu',r'D:\workspace\Baymax_Proxy\project\tmp\20171117\pixiu_3.zip')
# shutil.copytree(r'D:\workspace\Baymax_Proxy\project\tmp\20171118\report_channel_Tuniu_endpoint_68',
#                 r'D:\workspace\Baymax_Proxy\project\report\tuniu')
# shutil.copytree(r'D:\workspace\Baymax_Proxy\project\tmp\20171118\report_channel_Tuniu_endpoint_67',
#                 r'D:\workspace\Baymax_Proxy\project\report\tuniu', ignore=True)
# utility.copytree(r'D:\workspace\Baymax_Proxy\project\tmp\20171118\report_channel_Tuniu_endpoint_67',r'D:\workspace\Baymax_Proxy\project\report\tuniu')