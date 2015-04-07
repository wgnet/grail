from unittest import TestCase

from nose.tools import eq_

from grail import step
from tests.utils import validate_method_output


failure_exception = TestCase.failureException('Failure exception')
error_exception = Exception('Error exception')


@step
def passed_step():
    pass


@step
def failed_step():
    raise failure_exception


@step
def error_step():
    raise error_exception


def method_fail():
    passed_step()
    failed_step()
    raise Exception('we should not reach this')


@step(step_group=True)
def failed_group():
    passed_step()
    failed_step()
    raise Exception('we should not reach this too')


def method_fail_group():
    failed_group()
    raise Exception('we should not reach this even here')


def method_error():
    passed_step()
    error_step()
    raise Exception('we should not reach this')


@step(step_group=True)
def error_group():
    passed_step()
    error_step()
    raise Exception('we should not reach this too')


def method_error_group():
    error_group()
    raise Exception('we should not reach this even here')


class TestDirectHandling(TestCase):
    def test_method_fail(self):
        try:
            validate_method_output(method_fail, 'PASSED passed step\n'
                                                'FAILED failed step')
        except Exception as inst:
            eq_(inst, failure_exception)

    def test_group_fail(self):
        try:
            validate_method_output(method_fail_group, 'FAILED failed group\n'
                                                      '  PASSED passed step\n'
                                                      '  FAILED failed step')
        except Exception as inst:
            eq_(inst, failure_exception)

    def test_method_error(self):
        try:
            validate_method_output(method_error, 'PASSED passed step\n'
                                                 'ERROR error step')
        except Exception as inst:
            eq_(inst, error_exception)

    def test_group_error(self):
        try:
            validate_method_output(method_error_group, 'ERROR error group\n'
                                                       '  PASSED passed step\n'
                                                       '  ERROR error step')
        except Exception as inst:
            eq_(inst, error_exception)
