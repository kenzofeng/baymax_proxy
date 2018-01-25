import ConfigParser
import tempfile
import git
import logging
import os
import shutil
import subprocess
import re
import sys

logname = ""

mswindows = (sys.platform == "win32")
TEMPDIR = os.path.join(tempfile.gettempdir(), "autobuild")
os.makedirs(TEMPDIR) if not os.path.exists(TEMPDIR) else 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_CONF = "config.ini"


def read_subprocess(sp):
    logger = logging.getLogger(logname)
    while True:
        log = sp.stdout.readline()
        logger.info(log)
        if sp.poll() is not None:
            break


def read_error_subprocess(sp):
    logger = logging.getLogger(logname)
    while True:
        log = sp.stdout.readline()
        logger.info(log)
        if sp.poll() is not None:
            break


def setvalue(conf, section, obj):
    options = conf.options(section)
    for op in options:
        setattr(obj, op, conf.get(section, op))


def setarg(obj, kwargs):
    for k, v in kwargs.iteritems():
        setattr(obj, k, v[0])


def mymakedir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def copydir(sourceDir, targetDir):
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(sourceF):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetF) or (
                    os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                open(targetF, "wb").write(open(sourceF, "rb").read())
        if os.path.isdir(sourceF):
            copydir(sourceF, targetF)


def copyfile(sourcefile, targetfile):
    shutil.copy(sourcefile, targetfile)


def remove_file(path):
    shutil.rmtree(path, True)
    if os.path.exists(path):
        if mswindows:
            os.system('rd/s/q %s' % path)
        else:
            os.system('rm -rf %s' % path)


class Project(object):
    def __init__(self):
        self.projectdir = ""
        self.name = ""
        self.url = ""
        self.command = "build.bat qa"
        self.branch = ""
        self.package = ""
        self.sha = ""
        self.packages = []
        self.files = []
        self.basedir = ""

    def init(self):
        if type(self.packages) is str:
            self.packages = str(self.packages).split(',')
        if type(self.files) is str:
            self.files = str(self.files).split(',')
        if self.projectdir == "":
            self.projectdir = os.path.join(TEMPDIR, self.name)
        else:
            self.projectdir = os.path.join(self.projectdir, self.name)
        if hasattr(self, 'targetpath'):
            oldpath = os.getcwd()
            os.chdir(self.basedir)
            self.basedir = os.path.abspath(self.targetpath)
            os.chdir(oldpath)
        self.logger = logging.getLogger(logname)

    def remove(self):
        if os.path.exists(self.projectdir):
            shutil.rmtree(self.projectdir)

    def set_url(self):
        if hasattr(self, 'username'):
            url = "https://%s:%s@%s" % (self.username, self.password, self.url.split("//")[-1])
            return url
        else:
            return self.url

    def git_clone(self):
        try:
            self.logger.info('git clone project:%s' % self.projectdir)
            if os.path.exists(self.projectdir):
                self.git_checkout_branch()
            else:
                self.git_config_ssl()
                git.Repo.clone_from(self.url, self.projectdir)
                self.git_checkout_branch()
            return True
        except Exception, e:
            self.logger.error(e)
            return self.re_clone()

    def re_clone(self):
        try:
            remove_file(self.projectdir)
            self.git_config_ssl()
            git.Repo.clone_from(self.url, self.projectdir)
            self.git_checkout_branch()
            return True
        except Exception, e:
            self.logger.error("re_clone error:%s" % e)
            return False

    def git_config_ssl(self):
        g = git.Git(TEMPDIR)
        g.execute(["git", "config", "--global", "http.sslVerify", "false"])

    def git_checkout_branch(self):
        g = git.Git(self.projectdir)
        self.logger.info('git pull project:%s' % self.name)
        if self.sha != "":
            self.logger.info('git checkout %s' % (self.sha))
            g.execute(["git", "checkout", self.sha])
        else:
            g.execute(["git", "checkout", self.branch])
            g.pull()
            self.logger.info('git checkout %s' % (self.branch))
            g.execute(["git", "config", "core.longpaths", "true"])
            g.clean('-xdf')
            g.execute(["git", "reset", "--hard"])
            if self.branch != "":
                g.checkout(self.branch)
        self.git_get_branch_sha()

    def git_get_branch_sha(self):
        repo = git.Repo(self.projectdir)
        if hasattr(repo, 'active_branch'):
            self.sha = repo.active_branch.commit.hexsha
            self.branch = repo.active_branch.name
        else:
            self.sha = repo.branches[0].commit.hexsha
            self.branch = repo.branches[0].name

    def build(self):
        self.logger.info('package project:%s' % self.name)
        os.chdir(self.projectdir)
        self.logger.info(self.command)
        sp = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        read_subprocess(sp)

    def movetoloacal(self):
        for p in self.packages:
            warpath = p.split(':')[0]
            war_unzip_name = p.split(':')[-1]
            srcpath = os.path.join(self.projectdir, warpath)
            srcpath_dir = os.path.dirname(srcpath)
            srcpath_file_war = os.path.basename(srcpath)
            if '$d' in srcpath_file_war:
                srcpath_file_war = srcpath_file_war.replace("$d", "\d.*")
                for i in os.listdir(srcpath_dir):
                    if os.path.isfile(os.path.join(srcpath_dir, i)):
                        p = re.compile(srcpath_file_war)
                        rs = p.findall(i)
                        if rs:
                            srcpath_file_war = rs[0]
                            break
            srcpath = os.path.join(srcpath_dir, srcpath_file_war)
            if not os.path.exists(srcpath):
                self.logger.error("File is not exists:%s" % srcpath)
                return False
            targetpath = os.path.join(self.basedir, war_unzip_name)
            mymakedir(targetpath)
            os.chdir(targetpath)
            command = 'jar -xvf %s' % srcpath
            self.logger.info(command)
            os.popen(command)
        for f in self.files:
            sourcefile = f.split(':')[0]
            filename = f.split(':')[-1]
            srcpath = os.path.join(self.projectdir, sourcefile)
            targetpath = os.path.join(self.basedir, filename)
            if os.path.isdir(srcpath):
                copydir(srcpath, targetpath)
            elif os.path.isfile(srcpath):
                copyfile(srcpath, targetpath)


def build(conffile, **kwargs):
    basedir = os.path.dirname(conffile)
    conf = ConfigParser.ConfigParser()
    conf.read(conffile)
    sections = conf.sections()
    for section in sections:
        p = Project()
        p.basedir = basedir
        setvalue(conf, section, p)
        setarg(p, kwargs)
        p.init()
        if p.git_clone():
            p.build()
        p.movetoloacal()
        return p.sha,p.branch
