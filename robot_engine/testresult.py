import os

from robot.api import ExecutionResult, ResultWriter


def merge_report(test_report_path, *report):
    result = ExecutionResult(*report, merge=True)
    writer = ResultWriter(result)
    writer.write_results(log=os.path.join(test_report_path, 'log'), output=os.path.join(test_report_path, 'output'),
                         report=os.path.join(test_report_path, 'report'))
