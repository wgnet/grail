# coding=utf-8
from grail.steps import GrailValidationException
from nose.tools import ok_, assert_raises
from unittest import TestCase

import grail.state
import grail.settings
from grail import step
from tests.utils import validate_method_output


class TestStepDisabling(TestCase):
    @step
    def disabled_step(self):
        print 'Some data'

    @step(log_output=True)
    def disabled_step_params(self):
        print 'Some data after params'

    def setUp(self):
        grail.settings.disable_steps = True

    def tearDown(self):
        grail.settings.disable_steps = False

    def test_step_disabling(self):
        validate_method_output(self.disabled_step, u'Some data')

    def test_step_disabling_with_params(self):
        validate_method_output(self.disabled_step_params, u'Some data after params')


class TestStepLogic(TestCase):
    @step(step_group=True)
    def some_step_group(self):
        self.step1()
        self.step2()

    @step
    def step1(self):
        pass

    @step
    def step2(self):
        pass

    @step
    def fail_step(self):
        ok_(False, 'Explicit error')

    @step
    def ignored_step(self):
        pass

    @step(step_group=True)
    def pass_fail_ignore_group(self):
        self.step1()
        self.fail_step()
        self.ignored_step()

    @step(step_group=True)
    def pass_pending_ignore_group(self):
        self.step1()
        self.pending_step()
        self.ignored_step()

    @step
    def incorrect_step_call(self):
        self.step1()

    @step(treat_nested_steps_as_methods=True)
    def explicit_step_call_skip(self):
        self.step1()

    @step(step_group=True, treat_nested_steps_as_methods=True)
    def incorrect_step_group(self):
        self.step1()
        self.step2()

    def setUp(self):
        grail.state.is_test_wrapped = True

    def tearDown(self):
        grail.state.reset()

    def test_passed_flow(self):
        validate_method_output(self.some_step_group,
                               'PASSED some step group\n'
                               '  PASSED step1\n'
                               '  PASSED step2')

    def test_validation_flow(self):
        assert_raises(GrailValidationException, self.incorrect_step_call)

    def test_explicit_disable(self):
        validate_method_output(self.explicit_step_call_skip,
                               'PASSED explicit step call skip')

    def test_impossibility_to_disable_in_group(self):
        assert_raises(GrailValidationException, self.incorrect_step_group)

    def test_three_statuses(self):
        validate_method_output(self.pass_fail_ignore_group, 'FAILED pass fail ignore group\n'
                                                            '  PASSED step1\n'
                                                            '  FAILED fail step: Explicit error\n'
                                                            '  IGNORED ignored step')

    def method_with_two_groups(self):
        self.pass_fail_ignore_group()
        self.pass_fail_ignore_group()

    def test_ingore_output(self):
        validate_method_output(self.method_with_two_groups, 'FAILED pass fail ignore group\n'
                                                            '  PASSED step1\n'
                                                            '  FAILED fail step: Explicit error\n'
                                                            '  IGNORED ignored step\n'
                                                            'IGNORED pass fail ignore group')

    def test_pending_status(self):
        validate_method_output(self.pass_pending_ignore_group, 'PENDING pass pending ignore group\n'
                                                               '  PASSED step1\n'
                                                               '  PENDING pending step\n'
                                                               '  IGNORED ignored step')

    def test_failed_group(self):
        assert_raises(GrailValidationException, self.failed_group)

    @step(step_group=True)
    def failed_group(self):
        raise Exception()

    @step(pending=True)
    def pending_step(self):
        pass


class TestLogOutput(TestCase):
    @step
    def step_with_output(self):
        return 'Printed data'

    @step(log_output=False)
    def step_with_disabled_output(self):
        return 'Should not be shown'

    def test_enabled_output(self):
        validate_method_output(self.step_with_output, 'PASSED step with output -> Printed data')

    def test_disabled_output(self):
        validate_method_output(self.step_with_disabled_output, 'PASSED step with disabled output')


class TestLogInput(TestCase):
    @step
    def step_with_logged_input(self, input):
        pass

    @step(log_input=False)
    def step_with_not_logged_input(self, input):
        pass

    def test_enabled_input_logging(self):
        validate_method_output(self.step_with_logged_input, 'PASSED step with logged input (data)', ['data'])

    def test_disabled_input_logging(self):
        validate_method_output(self.step_with_not_logged_input, 'PASSED step with not logged input', ['data'])


class TestUnicode(TestCase):
    @step
    def step_with_returning_unicode(self):
        return u'Привет!!!'

    def test_returning_unicode(self):
        validate_method_output(self.step_with_returning_unicode, u'PASSED step with returning unicode -> Привет!!!')
