#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementations of WFST algorithms

"""
from collections import namedtuple
from heapq import heappush, heappop

from . import *

def extendfinal(wfst):
    """Modifies the input...
    """
    final_states = [s for s in wfst.st if is_final(wfst, s)]
    new_final = add_state(wfst, wfst.sr.one())
    #connect finals to new final
    for s in final_states:
        wt = wfst.st[s].wt
        wfst.st[s].ar.append(Arc(il=None, ol=None, wt=wt, nst=new_final))
        wfst.st[s] = State(ar=wfst.st[s].ar, wt=wfst.sr.zero())

def reversed(iwfst):
    """Builds a new wfst...

       Requires the input wfst to have a single final state
    """
    #Only one final state
    final_states = [s for s in iwfst.st if is_final(iwfst, s)]
    assert len(final_states) == 1
    #Build new wfst
    owfst = new_wfst(semiring=iwfst.sr)
    ##copy states
    for s in iwfst.st:
        add_state(owfst, with_id=s)
        if is_final(iwfst, s):
            owfst = make_with_start(owfst, s)
    set_finalweight(owfst, iwfst.st0, owfst.sr.one())
    ##make reversed arcs
    for s in iwfst.st:
        for arc in iwfst.st[s].ar:
            owfst.st[arc.nst].ar.append(Arc(il=arc.il, ol=arc.ol, wt=arc.wt, nst=s))
    return owfst

def dijkstra(iwfst):
    """Determine the shortest-distance from the starting state to each
       state (given that transitions contain no negative weights).
    """
    unvisited_states = []
    distances = {}
