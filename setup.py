#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as infh:
    long_description = infh.read()

version = "0.1.0"

python_requires = ">=3"

setup_args = {
    "name": "wfst",
    "version": version,
    "licence": "Apache/MIT",
    "description": "Weighted Finite State Transducers",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "author": "Daniel van Niekerk",
    "author_email": "dvn.demitasse@gmail.com",
    "url": "https://github.com/demitasse/wfstpy",
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
