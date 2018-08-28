#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementations of WFST algorithms

"""
from collections import defaultdict
from heapq import heappush, heappop

from . import *

def extendfinal(wfst):
    """MODIFIES THE INPUT...
    """
    final_states = [s for s in wfst.st if is_final(wfst, s)]
    new_final = add_state(wfst, wfst.W.one(), with_id=0)
    #connect finals to new final
    for s in final_states:
        wt = wfst.st[s].wt
        wfst.st[s].ar.append(Arc(il=None, ol=None, wt=wt, nst=new_final))
        wfst.st[s] = State(ar=wfst.st[s].ar, wt=wfst.W.zero())
    return wfst


def reversedfst(iwfst):
    """BUILDS A NEW WFST, THE INPUT WILL NOT BE MODIFIED...

       Requires the input WFST to have a single final state
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


def dijkstra(iwfst):
    """DOES NOT MODIFY THE INPUT...

       Determine the "shortest-distance" (smallest path weight) from the
       starting state to each state (given that transitions contain no
       negative weights).
    """
    distance = defaultdict(iwfst.W.zero)
    distance[iwfst.st0] = iwfst.W.one()
    #previous_state = {iwfst.st0: None}
    queue = [(iwfst.W.one(), iwfst.st0)]
    visited_states = set()

    while queue:
        path_weight, current_state = heappop(queue)
        if current_state not in visited_states:
            visited_states.add(current_state)
            for arc in iwfst.st[current_state].ar:
                arc_weight, next_state = arc.wt, arc.nst
                this_distance = path_weight * arc_weight  # product ⊗
                if this_distance < distance[next_state]:
                    distance[next_state] = this_distance
                    #previous_state[next_state] = current_state
                    heappush(queue, (this_distance, next_state))
    return dict(distance)


def nbest(wfst, n):
    """MODIFIES THE INPUT...

       Return a WFST representing the n-shortest paths. See Mohri & Riley,
       (2002) "An efficient algorithm for the n-best-strings problem"
    """
    shortest_distances = dijkstra(wfst) #will become φ[q] for rwfst
    print("SHORTEST_DISTANCES")
    for k, v in shortest_distances.items():
        print(k, v)
    wfst = extendfinal(wfst)
    rwfst = reversedfst(wfst)
    print("EXTENDED REVERSED:")
    import wfst.io as io
    print("".join(io.to_fsm_format(rwfst)))
    print("Find shortest distance for new superinitial in reversed")
    d = rwfst.W.zero()
    for arc in rwfst.st[rwfst.st0].ar:
        if arc.nst in shortest_distances:
            d = d + (arc.wt * shortest_distances[arc.nst])  # minimum of path combined with arc weight
    shortest_distances[rwfst.st0] = d
    for k, v in shortest_distances.items():
        print(k, v)
    print()
    ## SETUP ALGORITHM
    _debug = 0
    print("Create owfst and pairs mapping")
    owfst = new_wfst(semiring=wfst.W)
    st0 = add_state(owfst, with_id=_debug); _debug += 1
    owfst = make_with_start(owfst, st0)
    final_state = add_state(owfst, weight=owfst.W.one(), with_id=_debug); _debug += 1
    # Each state in `owfst` corresponds to a path with weight w from
    # the initial state of `rwfst` to a state s in `rwfst`, that can
    # be characterized by a pair (s, w). The dict `pairs` maps states
    # in `owfst` to the corresponding pair (s, w).
    pairs = {}
    # The superfinal state is denoted by `None`. The distance from the
    # superfinal state to the final state is `W.one()`, so
    # `shortest_distances[None]` is not needed.
    pairs[owfst.st0] = (None, owfst.W.zero())
    pairs[final_state] = (rwfst.st0, owfst.W.one())
    for k, v in pairs.items():
        print(k, v)
    print()
    ## COMPARISON STUFF
    def p_weight(state):
        if state is None:
            return rwfst.W.one()
        elif state in shortest_distances:
            return shortest_distances[state]
        else:
            return rwfst.W.zero()
    
    class ComparableState(object):
        def __init__(self, state):
            self.state = state

        def __lt__(self, other: "ComparableState"):
            px = pairs[self.state]
            py = pairs[other.state]
            wx = p_weight(px[0]) * px[1]
            wy = p_weight(py[0]) * py[1]
            print("\t\t\t\tpx =", px)
            print("\t\t\t\tpy =", py)
            print("\t\t\t\twx =", wx)
            print("\t\t\t\twy =", wy)
            if (py[0] is None) and (px[0] is not None):
                rval = (wx < wy) or (wy == wx)
                print("\t\t\t\t\t RETURN wx <= wy:", rval)
                return rval
            elif (px[0] is None) and (py[0] is not None):
                rval = wx < wy
                print("\t\t\t\t\t RETURN wx < wy:", rval)                
                return rval
            else:
                rval = wx < wy
                print("\t\t\t\t\t RETURN wx < wy:", rval)                
                return rval

        def __str__(self):
            return str(self.state)
    
    # r[s + 1], s state in fst, is the number of states in owfst which
    # corresponding pair contains s, i.e., it is number of paths
    # computed so far to s. Valid for s == None (the superfinal
    # state).
    r = defaultdict(int)
    queue = [ComparableState(final_state)]
    while queue:
        state = heappop(queue).state
        pstate, pweight = pairs[state]
        print("New iter,", "state:", state, "pair:", pstate, pweight)
        d = (rwfst.W.one() if pstate is None
             else shortest_distances[pstate] if pstate in shortest_distances
             else rwfst.W.zero())
        print("\td =", d)
        r[pstate] += 1
        for k in sorted(r, key=lambda x:x if type(x) is int else -1):
            kk = -1 if k is None else k
            print("\tr[", kk+1, "] =", r[k])
        if pstate is None:
            print("ADDING ARC TO STARTING STATE")
            owfst.st[st0].ar.append(Arc(il=None, ol=None, wt=owfst.W.one(), nst=state))
            print("ADDING ARC:", st0, None, None, owfst.W.one(), state)
        if pstate is None and r[pstate] == n:
            break
        if r[pstate] > n:
            continue
        if pstate is None:
            continue
        for rarc in rwfst.st[pstate].ar:
            arc = Arc(il=rarc.il, ol=rarc.ol, wt=rarc.wt, nst=rarc.nst)
            w = pweight * arc.wt
            nextstate = add_state(owfst, with_id=_debug); _debug += 1
            print("ADDING STATE:", nextstate)
            pairs[nextstate] = (arc.nst, w)
            owfst.st[nextstate].ar.append(arc)
            print("ADDING ARC", nextstate, rarc.il, rarc.ol, rarc.wt, state, sep=", ")
            heappush(queue, ComparableState(nextstate))
        if is_final(rwfst, pstate):
            final_weight = rwfst.st[pstate].wt
            w = pweight * final_weight
            nextstate = add_state(owfst, with_id=_debug); _debug += 1
            print("ADDING STATE:", nextstate)
            pairs[nextstate] = (None, w)
            owfst.st[nextstate].ar.append(Arc(il=None, ol=None, wt=final_weight, nst=state))            
            print("ADDING ARC", nextstate, None, None, final_weight, state, sep=", ")
            heappush(queue, ComparableState(nextstate))
        for k in sorted(pairs):
            print("\t", k, pairs[k])
        print()
    return owfst
    #before connect
    # for s in owfst.st:
    #     print("State:", s)
    #     for a in owfst.st[s].ar:
    #         print("\tArc:", a)
