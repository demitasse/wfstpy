#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of input and output functions
"""
from typing import Iterable, Optional

from . import Wfst, TropicalWeight


def to_fsm_format_walk(wfst, map_syms=False, map_states=False):
    s = wfst.get_start()
    if map_states:
        s_map = CallableDict()
        s_map[s] = len(s_map)
    else:
        s_map = lambda x:x
    s_queue = [s]
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
        if wfst.is_final(s):
            finals.append(s)
        for arc in wfst.arcs(s):
            if map_states:
                if arc.next_state not in s_map:
                    s_map[arc.next_state] = len(s_map)
            if arc.next_state not in s_done and arc.next_state not in s_queue:
                s_queue.append(arc.next_state)
            if map_syms and arc.ilabel not in sym_map:
                sym_map[arc.ilabel] = len(sym_map)
            if map_syms and arc.olabel not in sym_map:
                sym_map[arc.olabel] = len(sym_map)
            yield "\t".join(map(str, [s_map(s),
                                      s_map(arc.next_state),
                                      sym_map(arc.ilabel),
                                      sym_map(arc.olabel),
                                      arc.weight]))
    #FINAL STATES
    for s in finals:
        if wfst.get_finalweight(s) == wfst.W.one():
            yield str(s_map(s))
        else:
            yield str("\t".join(map(str, [s_map(s), wfst.get_finalweight(s)])))


def from_fsm_format(lines: Iterable[str],
                    semiring=TropicalWeight,
                    isyms: Optional[dict]=None,
                    osyms: Optional[dict]=None,
                    int_states=True,
                    epsilon="0"):
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
            ilabel = isyms[fields[2]] if isyms else None if fields[2] == epsilon else fields[2]
            olabel = osyms[fields[3]] if osyms else None if fields[3] == epsilon else fields[3]
            arcs.append((src, tgt, ilabel, olabel, weight))
        else:
            tgt = _states[0]
            final_states[tgt] = weight
        if start_state is None:
            start_state = _states[0]

    return Wfst.from_spec(semiring, start_state, states, final_states, arcs)
