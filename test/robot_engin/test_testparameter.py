import unittest
from robot_engine.testparameter import set_robot_paramenter_to_argfile


class TestRun(unittest.TestCase):
    def setUp(self):
        self.source = r'/home/feng/derbysoftsvn/DStorage'
        self.args = '-v TESTSETUP:providerConf-old'
        self.servercount = 1

    def test_set_parameter(self):
        set_robot_paramenter_to_argfile('/home/feng/', self.args)
