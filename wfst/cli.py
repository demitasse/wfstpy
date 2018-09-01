#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of command line tools
"""
import sys
import pickle

import click

from .io import to_fsm_format_walk, deserialise

@click.command()
@click.option("--map_syms", is_flag=True)
@click.option("--map_states", is_flag=True)
def wfstpy_print(map_syms, map_states):
    wfst = deserialise(sys.stdin.buffer.read())
    for line in to_fsm_format_walk(wfst, map_syms=map_syms, map_states=map_states):
        print(line, end="")
