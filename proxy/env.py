import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

mswindows = (sys.platform == "win32")
if mswindows:
    Doraemon = r'C:\Python27\Lib\site-packages\Doraemon'
else:
    Doraemon = r'/usr/local/lib/python2.7/site-packages/Doraemon'

opath = os.getcwd()
project = 'project'
test = os.path.join(BASE_DIR, project, 'test_automation')
report = os.path.join(BASE_DIR, project, 'report')
log = os.path.join(BASE_DIR, project, 'log')
tmp = os.path.join(BASE_DIR, project, 'tmp')

if not os.path.exists(test):
    os.makedirs(test)
if not os.path.exists(report):
    os.makedirs(report)
if not os.path.exists(log):
    os.makedirs(log)
if not os.path.exists(tmp):
    os.makedirs(tmp)

log_html = 'log.html'
report_html = 'report.html'
output_xml = 'output.xml'
deps = 'deps'
email = os.path.join(BASE_DIR, project, 'email.xml')


SENDER = "Automation_Regression_System@derbygroupmail.com"
SMPT = 'mail.derbygroupmail.com'
USERNAME = "warrior@derbygroupmail.com"
PWD = 'oWpR7svZHm3rxapF'