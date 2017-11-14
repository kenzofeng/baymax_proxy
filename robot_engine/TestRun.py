
from robot.api import TestData,TestDataDirectory,TestCaseFile



class TestRun(object):
    def __init__(self,servercount=1,source=''):
        self.servercount = servercount
        self.RunCase = [[] for row in range(self.servercount)]
        self.alltests = []
        self.TestSuit=TestData(source=source)
        self.testdir = ''
        self.testcasefile = ''
        self.get_all_test(self.TestSuit)
        self.distribut_test()

    def get_all_test(self,suite):
        if type(suite) is TestDataDirectory:
            self.testdir = suite.name
        elif type(suite) is TestCaseFile:
            self.testcasefile = suite.name
        for test in suite.testcase_table:
            self.alltests.append("%s.%s.%s" % (self.testdir, self.testcasefile, test.name))
        for child in suite.children:
            self.get_all_test(child)

    def distribut_test(self):
        i = 0
        for test in self.alltests:
            if i == self.servercount:
                i = 0
            self.RunCase[i].append(test)
            i += 1