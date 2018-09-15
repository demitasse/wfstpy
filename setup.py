#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = "0.1.0"

python_requires = ">=3"

setup_args = {
    "name": "wfst",
    "version": version,
    "description": "Weighted Finite State Transducers",
    "long_description": "Weighted Finite State Transducers and algorithms.",
    "author": "Daniel van Niekerk",
    "author_email": "dvn.demitasse@gmail.com",
    "url": "https://bitbucket.org/dvndemitasse/wfstpy",
    "packages": find_packages(),
    "test_suite": "tests",
    "python_requires": python_requires,
    "entry_points": {
        "console_scripts": [
            "wfst_print=wfst.cli:wfst_print"
        ]
    }
}

setup(**setup_args)
