#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file contains portions of code ported from OpenFst
# (http://www.openfst.org) under the following licence and
# attribution:
#
# """
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2005-2010 Google, Inc.
# """

"""This implements the n-best strings algorithm described by:

      Mohri, M. and Riley, M. 2002. An efficient algorithm for the
      n-best-strings problem. In Proc. ICSLP.
"""
from collections import defaultdict
from heapq import heappush, heappop

from .. import Wfst
from . import dijkstra, extendfinal, reversedfst


def _nbest(rwfst, phi, n):
    """Implements the core part of the algorithm building the output WFST
       in reverse
    """
    ## SETUP ALGORITHM
    _debug = 0
    print("Create owfst and pairs mapping")  #REM
    owfst = Wfst(semiring=rwfst.W)
    st0 = owfst.add_state(with_id=_debug); _debug += 1
    owfst.set_start(st0)
    final_state = owfst.add_state(weight=owfst.W.one(), with_id=_debug); _debug += 1
    # Each state in `owfst` corresponds to a path with weight w from
    # the initial state of `rwfst` to a state s in `rwfst`, that can
    # be characterized by a pair (s, w). The dict `pairs` maps states
    # in `owfst` to the corresponding pair (s, w).
    pairs = {}
    # The superfinal state is denoted by `None`. The distance from the
    # superfinal state to the final state is `W.one()`, so
    # `phi[None]` is not needed.
    pairs[owfst.get_start()] = (None, owfst.W.zero())
    pairs[final_state] = (rwfst.get_start(), owfst.W.one())
    for k, v in pairs.items(): #REM
        print(k, v)            #REM
    print()                    #REM
    ### DEFINE STATE COMPARISON
    def p_weight(state):
        if state is None:
            return rwfst.W.one()
        elif state in phi:
            return phi[state]
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
            print("\t\t\t\tpx =", px) #REM
            print("\t\t\t\tpy =", py) #REM
            print("\t\t\t\twx =", wx) #REM
            print("\t\t\t\twy =", wy) #REM
            if (py[0] is None) and (px[0] is not None):
                rval = (wx < wy) or (wy == wx)
                print("\t\t\t\t\t RETURN wx <= wy:", rval) #REM
                return rval
            elif (px[0] is None) and (py[0] is not None):
                rval = wx < wy
                print("\t\t\t\t\t RETURN wx < wy:", rval)  #REM          
                return rval
            else:
                rval = wx < wy
                print("\t\t\t\t\t RETURN wx < wy:", rval)  #REM           
                return rval

        def __str__(self):
            return str(self.state)
    ### END DEFINE STATE COMPARISON
    
    # r[s + 1], s state in fst, is the number of states in owfst which
    # corresponding pair contains s, i.e., it is number of paths
    # computed so far to s. Valid for s == None (the superfinal
    # state).
    r = defaultdict(int)
    queue = [ComparableState(final_state)]
    while queue:
        state = heappop(queue).state
        pstate, pweight = pairs[state]
        print("New iter,", "state:", state, "pair:", pstate, pweight) #REM
        d = (rwfst.W.one() if pstate is None
             else phi[pstate] if pstate in phi
             else rwfst.W.zero())
        print("\td =", d) #REM
        r[pstate] += 1
        for k in sorted(r, key=lambda x:x if type(x) is int else -1):
            kk = -1 if k is None else k
            print("\tr[", kk+1, "] =", r[k])                             #REM
        if pstate is None:
            print("ADDING ARC TO STARTING STATE")                        #REM
            owfst.add_arc(state=st0, next_state=state, ilabel=None, olabel=None, weight=owfst.W.one())
            print("ADDING ARC:", st0, None, None, owfst.W.one(), state)  #REM
        if pstate is None and r[pstate] == n:
            break
        if r[pstate] > n:
            continue
        if pstate is None:
            continue
        for rarc in rwfst.arcs(pstate):
            w = pweight * rarc.weight
            nextstate = owfst.add_state(with_id=_debug); _debug += 1
            print("ADDING STATE:", nextstate)                                          #REM
            pairs[nextstate] = (rarc.next_state, w)
            owfst.add_arc(state=nextstate, next_state=state,
                          ilabel=rarc.ilabel, olabel=rarc.olabel,
                          weight=rarc.weight)
            print("ADDING ARC", nextstate, rarc.ilabel, rarc.olabel, rarc.weight, state, sep=", ") #REM
            heappush(queue, ComparableState(nextstate))
        if rwfst.is_final(pstate):
            final_weight = rwfst.get_finalweight(pstate)
            w = pweight * final_weight
            nextstate = owfst.add_state(with_id=_debug); _debug += 1
            print("ADDING STATE:", nextstate)                                          #REM
            pairs[nextstate] = (None, w)
            owfst.add_arc(state=nextstate, next_state=state, ilabel=None, olabel=None, weight=final_weight)
            print("ADDING ARC", nextstate, None, None, final_weight, state, sep=", ")  #REM
            heappush(queue, ComparableState(nextstate))
        for k in sorted(pairs):         #REM
            print("\t", k, pairs[k])    #REM
        print()                         #REM
    return owfst
    #before connect                     #REM
    # for s in owfst.st:                #REM
    #     print("State:", s)            #REM
    #     for a in owfst.st[s].ar:      #REM
    #         print("\tArc:", a)        #REM
    


def nbest(wfst, n):
    """MODIFIES THE INPUT...

       Return a WFST representing the n-shortest paths.
    """
    shortest_distances = dijkstra(wfst) #will become φ[q] for rwfst
    print("SHORTEST_DISTANCES")             #REM
    for k, v in shortest_distances.items(): #REM
        print(k, v)                         #REM
    wfst = extendfinal(wfst)
    rwfst = reversedfst(wfst)
    print("EXTENDED REVERSED:")                                      #REM
    import wfst.io as io                                             #REM
    print("\n".join(io.to_fsm_format_walk(rwfst)))                   #REM
    print("Find shortest distance for new superinitial in reversed") #REM
    d = rwfst.W.zero()
    for arc in rwfst.arcs(rwfst.get_start()):
        if arc.next_state in shortest_distances:
            d = d + (arc.weight * shortest_distances[arc.next_state])  # minimum of path combined with arc weight
    shortest_distances[rwfst.get_start()] = d
    for k, v in shortest_distances.items():  #REM
        print(k, v)                          #REM
    print()                                  #REM
    return _nbest(rwfst, shortest_distances, n)
