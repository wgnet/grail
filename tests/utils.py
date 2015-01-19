from nose.tools import ok_


def validate_method_output(method, expected_output, args=(), kwargs={}):
    import sys
    from StringIO import StringIO

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out
    try:
        method(*args, **kwargs)
    except:
        output = out.getvalue().strip()
        ok_(output == expected_output, 'Unexpected stdout:\n%s' % output)
        sys.stdout = saved_stdout
        raise
