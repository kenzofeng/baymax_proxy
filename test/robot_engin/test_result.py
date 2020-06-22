import os

from robot.api import ExecutionResult, ResultWriter

report = ""
test_report_path = ""
result = ExecutionResult(report, merge=True)
writer = ResultWriter(result)
writer.write_results(log=os.path.join(test_report_path, 'log'), output=os.path.join(test_report_path, 'output'),
                     report=os.path.join(test_report_path, 'report'))
