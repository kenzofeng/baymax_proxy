import os
from collections import namedtuple

from robot.api import ExecutionResult, ResultWriter
from robot.errors import DataError
from robot.output import LOGGER
from robot.utils import unic

settings = namedtuple('Settings', ('output', 'xunit', 'report', 'log'))


class MyResultWrite(ResultWriter):

    def _write(self, name, writer, path, *args):
        try:
            writer(path, *args)
        except DataError as err:
            LOGGER.error(err.message)
        except EnvironmentError as err:
            # `err.filename` can be different than `path` at least if reading
            # log/report templates or writing split log fails.
            # `unic` is needed due to http://bugs.jython.org/issue1825.
            LOGGER.error("Writing %s file '%s' failed: %s: %s" %
                         (name.lower(), path, err.strerror, unic(err.filename)))
        else:
            pass


def merge_report(test_report_path, *report):
    result = ExecutionResult(*report, merge=True)
    writer = MyResultWrite(result)
    writer.write_results(log=os.path.join(test_report_path, 'log'), output=os.path.join(test_report_path, 'output'),
                         report=os.path.join(test_report_path, 'report'))
