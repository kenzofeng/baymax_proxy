import os
from collections import namedtuple

from robot.api import ExecutionResult, ResultWriter

settings = namedtuple('Settings', ('output', 'xunit', 'report', 'log'))


class MyExecutionResult(ExecutionResult):

    def _write(self, name, writer, path, *args):
        pass


def merge_report(test_report_path, *report):
    result = MyExecutionResult(*report, merge=True)
    writer = ResultWriter(result)
    writer.write_results(log=os.path.join(test_report_path, 'log'), output=os.path.join(test_report_path, 'output'),
                         report=os.path.join(test_report_path, 'report'))
