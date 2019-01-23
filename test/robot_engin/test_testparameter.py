import unittest
from robot_engine.testparameter import set_robot_paramenter_to_argfile
from robot_engine.testrun import TestRun


class TestTestRun(unittest.TestCase):
    def setUp(self):
        self.source = r'/home/feng/derbysoft_git/agoda-endpoint'
        self.args = '-s agoda-endpoint.ModifyReservation'
        self.servercount = 1

    def test_set_parameter(self):
        set_robot_paramenter_to_argfile('/home/feng/', self.args)

    def test_testrun(self):
        TestRun(servercount=1, source=self.source, args=self.args)
        # set_robot_paramenter_to_argfile('/home/feng/', self.args)
