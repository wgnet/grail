step_first_error = None
pending_step = False
indentation = ''
step_execution_started = False
treat_nested_steps_as_methods_global = False
step_exception_traceback = None
step_stack = None
is_test_wrapped = False


def reset():
    global step_first_error
    global pending_step
    global indentation
    global step_execution_started
    global treat_nested_steps_as_methods_global
    global step_exception_traceback
    global step_stack
    global is_test_wrapped
    step_first_error = None
    pending_step = False
    indentation = ''
    step_execution_started = False
    treat_nested_steps_as_methods_global = False
    step_exception_traceback = None
    step_stack = None
    is_test_wrapped = False
