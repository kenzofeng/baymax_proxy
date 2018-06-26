# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from testrun import TestRun


def create_argfile(testpath,runtests):
    argfiel_path = os.path.join(testpath, 'argfile.txt')
    f = open(argfiel_path, 'wb')
    for rt in runtests:
        f.write('\n')
        f.write('--test')
        f.write('\n')
        f.write(rt)
    f.close()


def create_argfile_parameter(testpath, robot_parameter):
    argfiel_path = os.path.join(testpath, 'argfile.txt')
    f = open(argfiel_path, 'wb')
    robot_parameters = robot_parameter.split(' ')
    for rt in robot_parameters:
        f.write('\n')
        f.write(rt)
        f.write('\n')
    f.close()
