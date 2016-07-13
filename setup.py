from setuptools import setup

version = '1.0.11.1'

setup(
    name='grail',
    version=version,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    packages=[
        'grail',
    ],
    description='Grail is a library which allows test script creation based on steps. '
                'It helps to structure your tests and get rid of additional test documentation for your code.',
    include_package_data=True,
    author='Wargaming.NET',
    author_email='web_qa_auto@wargaming.net',
    url='https://github.com/wgnet/grail'
)
