# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from testrun import TestRun


def create_argfile(runtests, testpath):
    argfiel_path = os.path.join(testpath, 'argfile.txt')
    f = open(argfiel_path,'wb')
    for rt in runtests:
        f.write('\n')
        f.write('--test')
        f.write('\n')
        f.write(rt)
    f.close()