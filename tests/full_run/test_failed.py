import os
from unittest import TestCase
from grail import step
from grail.base_test import BaseTest
from nose.tools import eq_
from tests.utils import validate_method_output


class TestFailed(TestCase):

    class TestObjectFailed(BaseTest):
        to_raise = Exception('My Exception')

        def test_failed(self):
            self.failed_step()

        @step
        def failed_step(self):
            raise self.to_raise

    def test_failed(self):
        try:
            work_dir = os.getcwd()
            sep_symbol = '/'
            if '\\' in work_dir:
                sep_symbol = '\\'
            validate_method_output(self.TestObjectFailed('test_failed').test_failed,
                                   'FAILED failed step: My Exception\n'
                                   '  File "{0}/tests/full_run/test_failed.py", line 15, in test_failed\n'
                                   '    self.failed_step()\n'
                                   '  File "{0}/grail/steps.py", line 96, in _execute\n'
                                   '    output = step_info.run_function()\n'
                                   '  File "{0}/grail/step_info.py", line 48, in run_function\n'
                                   '    return self.function(*self.args, **self.kwargs)\n'
                                   '  File "{0}/tests/full_run/test_failed.py", line 19, in failed_step\n'
                                   '    raise self.to_raise'.replace('/', sep_symbol).format(os.getcwd()))
        except Exception as inst:
            eq_(inst, self.TestObjectFailed.to_raise)
