import traceback
import sys

import grail.state as state
import grail.settings as settings
from grail.step_info import StepInfo, StepResults


def _generate_step_stack():
    stack = traceback.extract_stack()
    step_index = next(i for i, e in enumerate(stack) if e[0].endswith('steps.py'))
    stack = stack[step_index - 1:]
    stack = filter(lambda e: not (e[0].endswith('steps.py') or e[0].endswith('step_info.py')), stack)
    return stack


class _RedirectOut(object):
    def __init__(self):
        self.temp = sys.stdout
        self.step_messages = []
        self.delimited_messages = []
        self.string = ''

    def write(self, s):
        if s.strip(' '):
            self.delimited_messages.append(s)
            if not s.strip('\n'):
                self.string = ''.join(self.delimited_messages)
                self.delimited_messages = []
                self.step_messages.append(self.string)

    def flush(self):
        pass

    def out_to_lst(self):
        sys.stdout = self

    def out_to_console(self):
        sys.stdout = self.temp

    def get_captured_output(self):
        return ''.join(map(lambda line: state.indentation + line, self.step_messages))


def _should_skip_step():
    if settings.disable_steps:
        return True
    for filename, line_number, func_name, text in traceback.extract_stack():
        if func_name in settings.skip_func:
            return True
    if state.treat_nested_steps_as_methods_global and state.step_execution_started:
        return True


class GrailValidationException(Exception):
    pass


def _validate_step_info(step_info):
    if step_info.step_group and step_info.treat_nested_steps_as_methods:
        raise GrailValidationException(u'Step logic disabling is not applicable for step groups')
    if not step_info.step_group and state.step_execution_started:
        raise GrailValidationException(u'Step is called from another step (without group): %s' %
                                       step_info.function.func_name)


def _execute(step_info):
    if _should_skip_step():
        return step_info.run_function()

    redirected_out = _RedirectOut()
    redirected_out.out_to_lst()
    state.indentation = state.indentation + settings.indentation_const

    _validate_step_info(step_info)
    output, result, exception_instance = None, None, None
    try:
        if state.pending_step or state.step_first_error is not None:
            result = StepResults.IGNORED
        elif step_info.pending:
            result = StepResults.PENDING
            state.pending_step = True
        else:
            if step_info.step_group:
                output = step_info.run_function()
                if state.step_first_error:
                    result = StepResults.FAILED
                elif state.pending_step:
                    result = StepResults.PENDING
                else:
                    result = StepResults.PASSED
            else:
                state.step_execution_started = True
                state.treat_nested_steps_as_methods_global = step_info.treat_nested_steps_as_methods
                if not settings.export_mode:
                    output = step_info.run_function()
                result = StepResults.PASSED
    except Exception as inst:
        if step_info.step_group:
            raise GrailValidationException(u'Unexpected exception from step group: %s' % inst)
        if isinstance(inst, GrailValidationException):
            raise
        result = StepResults.FAILED
        if not state.step_first_error:
            state.step_first_error = inst
            state.step_stack = _generate_step_stack()
            state.step_exception_traceback = sys.exc_info()[2]
            exception_instance = inst

    redirected_out.out_to_console()
    state.step_execution_started = False
    console_message = redirected_out.get_captured_output()
    state.indentation = state.indentation[:-len(settings.indentation_const)]
    print_message = step_info.get_description(output, result, exception_instance)
    if console_message:
        print_message += '\n'
        print_message += console_message.rstrip()
    print print_message
    return output


def step(func=None, description='', pending=False, step_group=False, format_description=False,
         treat_nested_steps_as_methods=False, log_output=True):

    step_info = StepInfo()

    def wrapper(*args, **kwargs):
        step_info.args = args
        step_info.kwargs = kwargs
        return _execute(step_info)

    def params_wrapper(function):
        step_info.function = function
        return wrapper

    if func is None:
        step_info.description = description
        step_info.pending = pending
        step_info.step_group = step_group
        step_info.format_description = format_description
        step_info.treat_nested_steps_as_methods = treat_nested_steps_as_methods
        step_info.log_output = log_output
        return params_wrapper
    else:
        step_info.function = func
    return wrapper
