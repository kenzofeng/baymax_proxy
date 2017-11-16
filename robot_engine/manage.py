# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import svn.local
import svn.remote

from proxy import env
import utility


def test_checkout(test):
    utility.logmsg(test.test_log.path, "checkout test automation from svn")
    testpath = os.path.join(env.test, test.name)
    if os.path.exists(testpath):
        utility.remove_file(testpath)
    os.mkdir(testpath)
    r = svn.remote.RemoteClient(test.testurl)
    r.checkout(testpath)
    l = svn.local.LocalClient(testpath)
    test.revision_number = l.info()['commit#revision']
    test.save()
