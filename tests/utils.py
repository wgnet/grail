from nose.tools import ok_


def validate_method_output(method, expected_output, args=(), kwargs={}):
    import sys
    from StringIO import StringIO

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    def verify_output():
        output = out.getvalue().strip()
        ok_(output == expected_output, 'Unexpected stdout:\n%s' % output)
        sys.stdout = saved_stdout

    try:
        method(*args, **kwargs)
    except:
        verify_output()
        raise
    verify_output()
