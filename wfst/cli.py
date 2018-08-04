#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of command line tools
"""
import sys
import pickle

import click

from .io import to_fsm_format, deserialise

@click.command()
def wfstpy_print():
    wfst = deserialise(sys.stdin.buffer.read())
    for line in to_fsm_format(wfst):
        print(line, end="")
