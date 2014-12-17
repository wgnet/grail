from setuptools import setup

version = '1.0.1'

setup(
    name='grail',
    version=version,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    packages=[
        'grail',
    ],
    include_package_data=True,
    author='Igor Khrol',
    author_email='i_khrol@wargaming.net',
    url='http://www.wargaming.net/',
    install_requires=[
        'nose==1.3.3',
    ],
)
