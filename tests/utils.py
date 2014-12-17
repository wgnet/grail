from nose.tools import ok_


def validate_method_output(method, expected_output, args=None, kwargs=None):
    import sys
    from StringIO import StringIO

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out
    try:
        if args and kwargs:
            method(*args, **kwargs)
        elif args:
            method(*args)
        elif kwargs:
            method(**kwargs)
        else:
            method()
    finally:
        try:
            output = out.getvalue().strip()
            ok_(output == expected_output, 'Unexpected stdout:\n%s' % output)
        finally:
            sys.stdout = saved_stdout