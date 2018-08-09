#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple demonstration script
"""

from wfst import *
import wfst.algo as algo
from wfst.io import serialise, to_fsm_format


if __name__ == "__main__":
    wfst = new_wfst(TropicalWeight)
    #add states
    states = []
    for i in range(4):
        states.append(add_state(wfst))
    set_finalweight(wfst, states[-1], TropicalWeight(3.0))
    #add arcs
    wfst.st[states[0]].ar.append(Arc(il=1, ol=1, wt=wfst.W(3.0), nst=states[1]))
    wfst.st[states[0]].ar.append(Arc(il=4, ol=4, wt=wfst.W(5.0), nst=states[2]))
    wfst.st[states[1]].ar.append(Arc(il=2, ol=2, wt=wfst.W(2.0), nst=states[1]))
    wfst.st[states[1]].ar.append(Arc(il=3, ol=3, wt=wfst.W(4.0), nst=states[3]))
    wfst.st[states[2]].ar.append(Arc(il=5, ol=5, wt=wfst.W(4.0), nst=states[3]))
    #set starting state
    wfst = make_with_start(wfst, states[0])
    #serialise
    serialise(wfst, fname="original.wfst.pickle")

    print("ORIGINAL:")
    for line in to_fsm_format(wfst):
        print(line, end="")
    print()
    print("EXTEND FINAL:")
    algo.extendfinal(wfst)
    serialise(wfst, fname="extended.wfst.pickle")
    for line in to_fsm_format(wfst):
        print(line, end="")
    print()
    print("REVERSED:")
    rwfst = algo.reversed(wfst)
    serialise(rwfst, fname="reversed.wfst.pickle")
    for line in to_fsm_format(wfst):
        print(line, end="")

