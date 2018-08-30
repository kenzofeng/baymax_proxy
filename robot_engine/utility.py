import os
import random
import re
import signal
import smtplib
import zipfile
import zlib
from email.mime.text import MIMEText
import logging
import shutil
import requests
import tenjin
from lxml import etree
from django.utils import timezone
from proxy import env
import json
import paramiko

logger = logging.getLogger('django')
tenjin.set_template_encoding("utf-8")
from tenjin.helpers import *
import sys

mswindows = (sys.platform == "win32")
upload = 'upload'
upload_pwd = 'upload.derby'


def stop_job(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, upload, upload_pwd, timeout=10.0)
    stdin, stdout, stderr = ssh.exec_command("ps -ef|grep 'python -m' |awk '{print $2}'|xargs sudo kill -9")
    stdin, stdout, stderr = ssh.exec_command("ps -ef|grep 'java -jar' |awk '{print $2}'|xargs sudo kill -9")
    ssh.close()
    return "scuess"


def getip(instance_id):
    res = requests.get("https://devops.dbaws.net/aws/getip/{}/".format(instance_id))
    if res.status_code == 200:
        instance = json.loads(res.content)
        return instance['public_ip'], instance['private_ip']
    else:
        return "", ""


def newlogger(name, logfilename):
    handler = logging.FileHandler(os.path.join(env.log, logfilename))
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def job_test_log(name, log):
    logger = logging.getLogger(name)
    logger.info(log)


def rendestring(string):
    if string != "":
        _variable_pattern = r'\$\{[^\}]+\}'
        match = re.findall(_variable_pattern, string)
        if match:
            for arg in match:
                string = string.replace(arg, str(get_variable_value(arg)))
        return string


def matchre(path):
    warpath = os.path.split(path)
    filelist = os.listdir(warpath[0])
    for f in filelist:
        if warpath[-1] == f:
            return os.path.join(warpath[0], f)
        pattern = re.compile(warpath[-1].replace('$', '\\'))
        match = pattern.match(f)
        if match:
            return os.path.join(warpath[0], match.group())


def get_variable_value(arg):
    if env.variables.has_key(arg):
        return env.variables[arg]
    else:
        return arg


def gettoday():
    return timezone.now().strftime('%Y%m%d')


def getnow():
    return timezone.now().strftime('%H%M%S')


def gettime():
    return timezone.now()


def mkdir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


def logmsgs(logpath, msgs):
    f = open(os.path.join(env.log, logpath), 'a')
    try:
        f.writelines(msgs)
        f.write('\n')
        f.close()
    except Exception, e:
        logger.error(e)
    finally:
        f.close()


def logmsg(logpath, msg):
    f = open(os.path.join(env.log, logpath), 'a')
    try:
        f.write(msg)
        f.write('\n')
        f.close()
    except Exception, e:
        logger.error(e)
    finally:
        f.close()


def get_result_fromxml(outputpath):
    tree = etree.parse(outputpath)
    root = tree.getroot()
    result = root.xpath('/robot/suite/status')
    status = result[0].attrib['status']
    return status


def remove_file(fpath):
    if os.path.exists(fpath):
        try:
            os.remove(fpath)
        except Exception:
            pass
        if mswindows:
            os.system('rd /S/Q %s' % fpath)
        else:
            os.system('rm -rf %s' % fpath)


def remove_dir(path):
    shutil.rmtree(path, True)
    if mswindows:
        os.system('rd /S/Q %s' % path)
    else:
        os.system('rm -rf %s' % path)


def save_test_log(test):
    try:
        log_path = os.path.join(env.log, test.job_test_result.log_path)
        f = open(log_path, 'rb')
        fstr = f.read()
        f.close()
        test_ds_all = test.job_test_distributed_result_set.all()
        for test_ds in test_ds_all:
            try:
                r = requests.get("http://%s/test/log/%s" % (test_ds.host, test_ds.pk), timeout=5)
                fstr = fstr + r.content
            except Exception, e:
                fstr = fstr + str(e)
        gzipstr = zlib.compress(fstr)
        test.job_test_result.log = gzipstr.encode("base64")
        test.job_test_result.save()
        remove_file(log_path)
    except Exception, e:
        print e


def save_log(job):
    log_path = os.path.join(env.log, job.job_log.path)
    f = open(log_path, 'rb')
    fstr = f.read()
    f.close()
    gzipstr = zlib.compress(fstr)
    job.job_log.text = gzipstr.encode("base64")
    job.job_log.save()
    remove_file(log_path)


def set_email(test, host):
    emailfile = env.email
    context = {
        "run_time": str(test.job.start_time),
        #                "job_number":test.job.job_number,
        "project": test.job.project,
        "Automation": test.name,
        'log': 'http://%s/job/test/log/%s' % (host, test.job_test_result.id),
        'test_version': test.revision_number,
        'result': test.status,
        'reportlink': 'http://%s/job/report/%s' % (host, test.id)}
    path = '\\'.join((emailfile.split('\\'))[:-1])
    engine = tenjin.Engine(path=[path], cache=tenjin.MemoryCacheStorage())
    emailstring = engine.render(emailfile, context)
    return str(emailstring)


def send_email(test, host):
    receiver = test.job.email
    if receiver != '':
        sender = env.SENDER
        subject = '%s_Regression_Test_%s' % (test.job.project, test.status)
        smtpserver = env.SMPT
        username = env.USERNAME
        password = env.PWD
        msg = MIMEText(set_email(test, host), 'html')
        msg['Subject'] = subject
        smtp = smtplib.SMTP_SSL(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()


def zip_file(sourcefile, targetfile):
    try:
        filelist = []
        if os.path.isfile(sourcefile):
            filelist.append(sourcefile)
        else:
            for root, dirs, files in os.walk(sourcefile):
                if '.svn' in root:
                    continue
                for name in files:
                    filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(targetfile, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(sourcefile):]
            zf.write(tar, arcname)
        zf.close()
    except Exception, e:
        logger.error(e)


def extract_zip(source, target):
    f = zipfile.ZipFile(source, 'r')
    for ff in f.namelist():
        f.extract(ff, target)


def random_str(randomlength=15):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def kill(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


def copytree(src, dst, symlinks=False):
    names = os.listdir(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)

    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                if os.path.isdir(dstname):
                    os.rmdir(dstname)
                elif os.path.isfile(dstname):
                    os.remove(dstname)
                shutil.copy2(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except OSError as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Exception(errors)


def conver_To_Boolean(value):
    if value.lower() == "true":
        return True
    else:
        return False
