#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of input and output functions
"""
from typing import Iterable, Optional
import pickle

from . import is_final, Wfst, TropicalWeight, new_wfst_from_spec


class CallableDict(dict):
    def __call__(self, key):
        return self[key]


def to_fsm_format_walk(wfst, map_syms=False, map_states=False):
    s = wfst.st0
    if map_states:
        s_map = CallableDict()
        s_map[s] = len(s_map)
    else:
        s_map = lambda x:x
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
            if map_states:
                if arc.nst not in s_map:
                    s_map[arc.nst] = len(s_map)
            if arc.nst not in s_done and arc.nst not in s_queue:
                s_queue.append(arc.nst)
            if map_syms and arc.il not in sym_map:
                sym_map[arc.il] = len(sym_map)
            if map_syms and arc.ol not in sym_map:
                sym_map[arc.ol] = len(sym_map)
            yield "\t".join(map(str, [s_map(s),
                                      s_map(arc.nst),
                                      sym_map(arc.il),
                                      sym_map(arc.ol),
                                      arc.wt]))
    #FINAL STATES
    for s in finals:
        if wfst.st[s].wt == wfst.W.one():
            yield str(s_map(s))
        else:
            yield str("\t".join(map(str, [s_map(s), wfst.st[s].wt])))


def from_fsm_format(lines: Iterable[str],
                    semiring=TropicalWeight,
                    isyms: Optional[dict]=None,
                    osyms: Optional[dict]=None,
                    int_states=True):
    start_state = None
    states = set()
    final_states = {}
    arcs = []
    for line in lines:
        fields = line.split()
        num_fields = len(fields)
        if num_fields == 1:
            _states, weight = fields[:1], semiring.one()
        elif num_fields == 2:
            _states, weight = fields[:1], semiring.from_str(fields[1])
        elif num_fields == 4:
            _states, weight = fields[:2], semiring.one()
        elif num_fields == 5:
            _states, weight = fields[:2], semiring.from_str(fields[4])
        else:
            raise Exception("Format error: wrong number of fields!")
        if int_states:
            _states = list(map(int, _states))
        if len(_states) == 2:
            src, tgt = _states
            states.add(src)
            states.add(tgt)
            ilabel = isyms[fields[2]] if isyms else fields[2]
            olabel = osyms[fields[3]] if osyms else fields[3]
            arcs.append((src, tgt, ilabel, olabel, weight))
        else:
            tgt = _states[0]
            final_states[tgt] = weight
        if start_state is None:
            start_state = _states[0]

    return new_wfst_from_spec(semiring, start_state, states, final_states, arcs)


def serialise(wfst, fname=None):
    if fname is None:
        return pickle.dumps(wfst)
    else:
        with open(fname, "wb") as outfh:
            pickle.dump(wfst, outfh)


def deserialise(s):
    wfst = pickle.loads(s)
    return wfst
