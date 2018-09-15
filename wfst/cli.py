#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of command line tools
"""
import sys
import pickle
import argparse

from .io import to_fsm_format_walk

def wfst_print():
    parser = argparse.ArgumentParser(description="Print out a compiled WFST (AT&T FSM format)")
    parser.add_argument("--map_syms", action="store_true", help="map symbols to integers (ε=0)")
    parser.add_argument("--map_states", action="store_true", help="map state IDs to integers")
    args = parser.parse_args()

    wfst = pickle.loads(sys.stdin.buffer.read())
    for line in to_fsm_format_walk(wfst, map_syms=args.map_syms, map_states=args.map_states):
        print(line)
