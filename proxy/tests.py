from robot.api import TestSuiteBuilder
from robot.run import RobotFramework
from robot.conf import RobotSettings

args = "--test Hilton_adapter.modifyReservation(json)-commit.TC02.167  --test Hilton_adapter.modifyReservation(json)-commit.TC02.169"
# args =args.strip()
# print args
source = r'D:\workspace\baymax_proxy\project\test_automation\Hilton_adapter'
rb = RobotFramework()
options, datasources = rb._parse_arguments(
    "{}".format(source).split(" ") if args == "" else "{} {}".format(args, source).split(" "))
settings = RobotSettings(options)
suite = TestSuiteBuilder(settings['SuiteNames'],
                         settings['WarnOnSkipped'],
                         settings['Extension']).build(*datasources)
suite.configure(**settings.suite_config)
suite = suite

RobotFramework().execute_cli(
    "--test Hilton_adapter.modifyReservation(json)-commit.TC02.167 D:\workspace\baymax_proxy\project\test_automation\Hilton_adapter",
    exit=exit)
