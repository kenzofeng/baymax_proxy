from collections import namedtuple
from git import Repo
from robot_engine.utility import mkdir,remove_file
# import unittest
#
#
# class TestCaseTest(unittest.TestCase):
#     def setUp(self):
#         Test = namedtuple('test', ['source_type', 'source_url', 'source_branch'])
#         self.test = Test('Git', 'http://52.34.81.222/warrior-qa/dstorage.git', 'master')
#         self.test_path = '/home/feng/derbysfot_git/Dstorage'
#
#     def test_git_checkout(self):
#         cloned_repo = Repo.clone(self.test.source_url, self.test_path)
#         print(cloned_repo)
Test = namedtuple('test', ['source_type', 'source_url', 'source_branch'])
test = Test('Git', 'http://52.34.81.222/warrior-qa/dstorage.git', 'master')
test_path = '/home/feng/derbysoft_git/Dstorage'
remove_file(test_path)
mkdir(test_path)
cloned_repo = Repo.clone_from(url=test.source_url, to_path=test_path)
branch = cloned_repo.git.checkout(test.source_branch)
commit = Repo(test_path).head.commit
print(commit)