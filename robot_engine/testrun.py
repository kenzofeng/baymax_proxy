from robot.api import TestSuiteBuilder
from robot.conf import RobotSettings
from robot.run import RobotFramework


class TestRun(object):
    def __init__(self, servercount=1, source='', args=""):
        try:
            self.source = source.strip()
            self.args = args.strip()
            self.suite = None
            self.servercount = servercount
            self.RunCase = [[] for row in range(self.servercount)]
            self.alltests = []
            self.testdir = ''
            self.testcasefile = ''
            self.count = ''
            self.init_rb()
            self.get_all_test(self.suite)
            self.distribut_test()
        except Exception as e:
            raise Exception("TestRun __init__ error:{}".format(e))

    def init_rb(self):
        try:
            rb = RobotFramework()
            options, datasources = rb.parse_arguments(list(filter(None, "{}".format(self.source).split(
                " ") if self.args == "" else "{} {}".format(self.args, self.source).split(" "))))
            settings = RobotSettings(options)
            suite = TestSuiteBuilder(settings['SuiteNames'],
                                     settings['WarnOnSkipped'],
                                     settings['Extension']).build(*datasources)
            suite.configure(**settings.suite_config)
            self.suite = suite
            self.count = self.suite.test_count
        except Exception as e:
            raise Exception("TestRun init_rb error:{}".format(e))

    def get_all_test(self, suite):
        for csuite in suite.suites:
            if csuite.suites:
                self.get_all_test(csuite)
            else:
                if csuite.tests:
                    for ctest in csuite.tests:
                        self.alltests.append("{}.{}".format(ctest.parent.longname, ctest.name))

    def distribut_test(self):
        i = 0
        for test in self.alltests:
            if i == self.servercount:
                i = 0
            self.RunCase[i].append(test)
            i += 1
