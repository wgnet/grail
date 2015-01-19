from unittest import TestCase
from grail import step
from tests.utils import validate_method_output

import grail.settings as settings
import grail.state as state


@step
def simple_step():
    pass


@step(pending=True)
def pending_step():
    pass


@step(description='Some Description')
def step_with_description():
    pass


@step
def step_with_params(some_string=None):
    print some_string


@step(description='Some info \'{0}\' {kw_str}', format_description=True)
def step_with_format_params(some_string, kw_str):
    print some_string
    print kw_str


@step(step_group=True)
def step_group():
    simple_step()
    pending_step()


@step
def step_with_args(*args):
    print args


@step
def step_with_kwargs(**kwargs):
    print kwargs


class TestExport(TestCase):
    def setUp(self):
        state.reset()
        settings.export_mode = True

    def tearDown(self):
        state.reset()
        settings.export_mode = False

    def test_simple_output(self):
        validate_method_output(simple_step, 'simple step')

    def test_pending_output(self):
        validate_method_output(pending_step, 'pending step')

    def test_description(self):
        validate_method_output(step_with_description, 'Some Description')

    def test_skip_none_params(self):
        validate_method_output(step_with_params, 'step with params')

    def test_print_args_params(self):
        validate_method_output(step_with_params, 'step with params (42)', args=('42',))

    def test_print_kwargs_params(self):
        validate_method_output(step_with_params, 'step with params (some_string=42)', kwargs={'some_string': '42'})

    def test_format_params(self):
        validate_method_output(step_with_format_params, 'Some info \'None\' kw42',
                               args=(None,),
                               kwargs={'kw_str': 'kw42'})

    def test_step_group(self):
        validate_method_output(step_group, 'step group\n'
                                           '  simple step\n'
                                           '  pending step')

    def test_step_with_args(self):
        validate_method_output(step_with_args, 'step with args', args=(None, None))

    def test_step_with_kwargs(self):
        validate_method_output(step_with_kwargs, 'step with kwargs (a=b)', kwargs={'a': 'b'})
