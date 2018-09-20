import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


SENDER = "Baymax@derbygroupmail.com"
SMPT = 'mail.dbaws.net'
USERNAME = "warrior@dbaws.net"
PWD = 'dDpWhhq8M4ogg__B8yZinzwahh'
email_port=465