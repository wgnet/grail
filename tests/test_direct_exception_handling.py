from unittest import TestCase
from nose.tools import eq_
from grail import step
from tests.utils import validate_method_output

failure_exception = Exception('Correct exception')


@step
def passed_step():
    pass


@step
def failed_step():
    raise failure_exception


def method_to_raise():
    passed_step()
    failed_step()
    raise Exception('we should not reach this')


class TestDirectHandling(TestCase):
    def test_direct_exception_handling(self):
        try:
            validate_method_output(method_to_raise, 'PASSED passed step\n'
                                                    'FAILED failed step')
        except Exception as inst:
            eq_(inst, failure_exception)