#!/usr/bin/env python3

import codecs
from setuptools import setup


def read_long_description():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError, RuntimeError):
        return ""


setup(
    name="ssmanager-nopanel",
    version="0.0.2",
    python_requires='~=3.6',
    description="ssmanager web daemon: support multi-methods & log traffic to influxdb",
    author='fzinfz',
    author_email='fzinfz@gmail.com',
    url='https://github.com/fzinfz/ssmanager-nopanel',
    packages=['ssmanager_nopanel'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'ssmanager-nopanel=ssmanager_nopanel.main:main'
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
    ],
    long_description=read_long_description(),
)
