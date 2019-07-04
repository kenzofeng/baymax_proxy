import logging
import os
from collections import namedtuple

from robot.api import ExecutionResult, ResultWriter
from robot.errors import DataError
from robot.output import LOGGER
from robot.utils import unic

settings = namedtuple('Settings', ('output', 'xunit', 'report', 'log'))

logger = logging.getLogger('django')


class MyResultWrite(ResultWriter):

    def _write(self, name, writer, path, *args):
        try:
            writer(path, *args)
        except DataError as err:
            logger.error("New MyResultWrite DataError:{}".format(err))
            LOGGER.error(err.message)
        except EnvironmentError as err:
            logger.error("New MyResultWrite EnvironmentError:{}".format(err))
            LOGGER.error("Writing %s file '%s' failed: %s: %s" %
                         (name.lower(), path, err.strerror, unic(err.filename)))
        else:
            pass


def merge_report(test_report_path, *report):
    logger.info("merge_report Start:{}".format(test_report_path))
    result = ExecutionResult(*report, merge=True)
    writer = MyResultWrite(result)
    logger.info("write_results Start:{}".format(test_report_path))
    writer.write_results(log=os.path.join(test_report_path, 'log'), output=os.path.join(test_report_path, 'output'),
                         report=os.path.join(test_report_path, 'report'))
    logger.info("merge_report End:{}".format(test_report_path))
