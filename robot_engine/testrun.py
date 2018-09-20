from robot.api import TestSuiteBuilder
from robot.run import RobotFramework
from robot.conf import RobotSettings


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
            self.init_rb()
            self.get_all_test(self.suite)
            self.distribut_test()
        except Exception as e:
            raise Exception(e)

    def init_rb(self):
        rb = RobotFramework()
        options, datasources = rb._parse_arguments(
            "{}".format(self.source).split(" ") if self.args == "" else "{} {}".format(self.args,
                                                                                       self.source).split(
                " "))
        settings = RobotSettings(options)
        suite = TestSuiteBuilder(settings['SuiteNames'],
                                 settings['WarnOnSkipped'],
                                 settings['Extension']).build(*datasources)
        suite.configure(**settings.suite_config)
        self.suite = suite


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
