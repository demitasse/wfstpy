#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple demonstration script
"""

from wfst import *
from wfst.algo import extendfinal
from wfst.io import serialise, to_fsm_format


if __name__ == "__main__":
    wfst = new_wfst()
    #add states
    states = []
    for i in range(4):
        states.append(add_state(wfst))
    set_finalweight(wfst, states[-1], 3.0)
    #add arcs
    wfst.st[states[0]].ar.append(Arc(il=1, ol=1, wt=3.0, nst=states[1]))
    wfst.st[states[0]].ar.append(Arc(il=4, ol=4, wt=5.0, nst=states[2]))
    wfst.st[states[1]].ar.append(Arc(il=2, ol=2, wt=2.0, nst=states[1]))
    wfst.st[states[1]].ar.append(Arc(il=3, ol=3, wt=4.0, nst=states[3]))
    wfst.st[states[2]].ar.append(Arc(il=5, ol=5, wt=4.0, nst=states[3]))
    #set starting state
    wfst = make_with_start(wfst, states[0])
    #serialise
    import pickle
    with open("example.wfst.pickle", "wb") as outfh:
        outfh.write(serialise(wfst))

    print("ORIGINAL:")
    print(to_fsm_format(wfst))
    print()
    print("EXTEND FINAL:")
    extendfinal(wfst)
    print(to_fsm_format(wfst))
