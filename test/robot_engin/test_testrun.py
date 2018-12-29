import unittest
from robot_engine.testrun import TestRun as MyTestRun


class TestRun(unittest.TestCase):
    def setUp(self):
        self.source = r'/home/feng/derbysoftsvn/DStorage'
        self.args = '-v TESTSETUP:providerConf-old'
        self.servercount = 1

    def test_set_subnet(self):
        testrun = MyTestRun(self.servercount, self.source, self.args)
        print(testrun)
