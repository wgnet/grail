import traceback
from functools import wraps
from unittest import TestCase

import grail.state as state
import grail.settings as settings


def handle_steps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            state.is_test_wrapped = True
            result = func(*args, **kwargs)

            step_first_error = state.step_first_error
            pending_step = state.pending_step
            step_exception_traceback = state.step_exception_traceback
            step_stack = state.step_stack
            state.reset()

            if step_first_error is not None:
                for line in step_stack:
                    print '  File "%s", line %i, in %s\n    %s' % line
                print ''.join(traceback.format_tb(step_exception_traceback))
                raise step_first_error, None, step_exception_traceback
            if pending_step and not settings.export_mode:
                raise Exception('Test is failed as there are pending steps')
            return result
        finally:
            state.is_test_wrapped = False

    return wrapper


class BaseTestMeta(type):
    def __new__(mcs, name, bases, attrs):
        test_functions = {k: handle_steps(v) for k, v in attrs.iteritems() if k.startswith("test") and callable(v)}
        attrs.update(test_functions)
        cls = super(BaseTestMeta, mcs).__new__(mcs, name, bases, attrs)
        return cls


class BaseTest(TestCase):
    __metaclass__ = BaseTestMeta
