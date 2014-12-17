import nose

if __name__ == '__main__':
    nose.run_exit(argv=['nosetests', '-v', '--exe',
                        'tests',
                        '--with-xunit',
                        '--xunit-file=grail_xunit_output.xml',
                        ])
