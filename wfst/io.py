#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of input and output functions
"""
import pickle

from . import is_final, Wfst


class CallableDict(dict):
    def __call__(self, key):
        return self[key]


def to_fsm_format(wfst, map_syms=False):
    s = wfst.st0
    s_map = {}
    s_map[s] = len(s_map)
    s_queue = [wfst.st0]
    finals = []
    if map_syms:
        sym_map = CallableDict()
        sym_map[None] = 0
    else:
        sym_map = lambda x:x
    s_done = set()
    #ARCS STARTING WITH START STATE
    while s_queue:
        s = s_queue.pop(0)
        s_done.add(s)
        if is_final(wfst, s):
            finals.append(s)
        for arc in wfst.st[s].ar:
            if arc.nst not in s_map:
                s_map[arc.nst] = len(s_map)
            if arc.nst not in s_done and arc.nst not in s_queue:
                s_queue.append(arc.nst)
            if map_syms and arc.il not in sym_map:
                sym_map[arc.il] = len(sym_map)
            if map_syms and arc.ol not in sym_map:
                sym_map[arc.ol] = len(sym_map)
            yield "\t".join(map(str, [s_map[s],
                                      s_map[arc.nst],
                                      sym_map(arc.il),
                                      sym_map(arc.ol),
                                      arc.wt])) + "\n"
    #FINAL STATES
    for s in finals:
        if wfst.st[s].wt == wfst.sr.one():
            yield str(s_map[s]) + "\n"
        else:
            yield str("\t".join(map(str, [s_map[s], wfst.st[s].wt]))) + "\n"


def serialise(wfst, fname=None):
    if fname is None:
        return pickle.dumps(wfst)
    else:
        with open(fname, "wb") as outfh:
            pickle.dump(wfst, outfh)
    

def deserialise(s):
    wfst = pickle.loads(s)
    return wfst
