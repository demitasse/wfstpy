#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementations of WFST algorithms

"""
from collections import defaultdict
from heapq import heappush, heappop

from .. import Wfst

def extendfinal(wfst):
    """MODIFIES THE INPUT...
    """
    final_states = [s for s in wfst.states() if wfst.is_final(s)]
    new_final = wfst.add_state(wfst.W.one(), with_id=0)
    #connect finals to new final with epsilon arcs
    for s in final_states:
        weight = wfst.get_finalweight(s)
        wfst.add_arc(state=s, next_state=new_final, ilabel=None, olabel=None, weight=weight)
        wfst.set_finalweight(s, wfst.W.zero())
    return wfst


def reversedfst(iwfst):
    """BUILDS A NEW WFST, THE INPUT WILL NOT BE MODIFIED...

       Requires the input WFST to have a single final state
    """
    #Only one final state
    final_states = [s for s in iwfst.states() if iwfst.is_final(s)]
    assert len(final_states) == 1
    #Build new wfst
    owfst = Wfst(semiring=iwfst.W)
    ##copy states
    for s in iwfst.states():
        owfst.add_state(with_id=s)
        if iwfst.is_final(s):
            owfst.set_start(s)
    owfst.set_finalweight(iwfst.get_start(), owfst.W.one())
    ##make reversed arcs
    for s in iwfst.states():
        for arc in iwfst.arcs(s):
            owfst.add_arc(state=arc.next_state, next_state=s,
                          ilabel=arc.ilabel, olabel=arc.olabel,
                          weight=arc.weight)
    return owfst


def dijkstra(iwfst):
    """DOES NOT MODIFY THE INPUT...

       Determine the "shortest-distance" (smallest path weight) from
       the starting state to each state (provided that transitions
       contain no negative weights).
    """
    distance = defaultdict(iwfst.W.zero)
    distance[iwfst.get_start()] = iwfst.W.one()
    #previous_state = {iwfst.get_start(): None}
    queue = [(iwfst.W.one(), iwfst.get_start())]
    visited_states = set()

    while queue:
        path_weight, current_state = heappop(queue)
        if current_state not in visited_states:
            visited_states.add(current_state)
            for arc in iwfst.arcs(current_state):
                this_distance = path_weight * arc.weight  # semiring product ⊗
                if this_distance < distance[arc.next_state]:
                    distance[arc.next_state] = this_distance
                    #previous_state[arc.next_state] = current_state
                    heappush(queue, (this_distance, arc.next_state))
    return dict(distance)
