#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementations of WFST algorithms

"""
from collections import defaultdict
from heapq import heappush, heappop

from . import *

def extendfinal(wfst):
    """Modifies the input...
    """
    final_states = [s for s in wfst.st if is_final(wfst, s)]
    new_final = add_state(wfst, wfst.W.one())
    #connect finals to new final
    for s in final_states:
        wt = wfst.st[s].wt
        wfst.st[s].ar.append(Arc(il=None, ol=None, wt=wt, nst=new_final))
        wfst.st[s] = State(ar=wfst.st[s].ar, wt=wfst.W.zero())


def reversed(iwfst):
    """Builds a new wfst...

       Requires the input wfst to have a single final state
    """
    #Only one final state
    final_states = [s for s in iwfst.st if is_final(iwfst, s)]
    assert len(final_states) == 1
    #Build new wfst
    owfst = new_wfst(semiring=iwfst.W)
    ##copy states
    for s in iwfst.st:
        add_state(owfst, with_id=s)
        if is_final(iwfst, s):
            owfst = make_with_start(owfst, s)
    set_finalweight(owfst, iwfst.st0, owfst.W.one())
    ##make reversed arcs
    for s in iwfst.st:
        for arc in iwfst.st[s].ar:
            owfst.st[arc.nst].ar.append(Arc(il=arc.il, ol=arc.ol, wt=arc.wt, nst=s))
    return owfst


def dijkstra(wfst):
    """Determine the "shortest-distance" (smallest path weight) from the
       starting state to each state (given that transitions contain no
       negative weights).

    """
    distance = defaultdict(wfst.W.zero)
    distance[wfst.st0] = wfst.W.one()
    #previous_state = {wfst.st0: None}
    queue = [(wfst.W.one(), wfst.st0)]
    visited_states = set()

    while queue:
        path_weight, current_state = heappop(queue)
        if current_state not in visited_states:
            visited_states.add(current_state)
            for arc in wfst.st[current_state].ar:
                arc_weight, next_state = arc.wt, arc.nst
                this_distance = path_weight * arc_weight  # product ⊗
                if this_distance < distance[next_state]:
                    distance[next_state] = this_distance
                    #previous_state[next_state] = current_state
                    heappush(queue, (this_distance, next_state))
    return dict(distance)
