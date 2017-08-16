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
    version="0.0.1",
    python_requires='~=3.0',
    description="A ssmanager simple http daemon without panel",
    author='fzinfz',
    author_email='fzinfz@gmail.com',
    url='https://github.com/fzinfz/ssmanager-nopanel',
    py_modules='ssmanager-nopanel.py',
    install_requires=[],
    entry_points={
        'console_scripts':[
            'ssmanager-nopanel-native=native:main'
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
    ],
    long_description=read_long_description(),
)
