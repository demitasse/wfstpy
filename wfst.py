#!/usr/bin/env python3
"""Simple implementation of WFST to test algorithms

"""
from uuid import uuid4 
from collections import namedtuple

Wfst = namedtuple("Wfst", "s0 s") #start, states
Arc = namedtuple("Arc", "i o w n") #ilabel, olabel, weight, nextstate
State = namedtuple("State", "a w") #arcs, weight

def add_state(wfst, w=None):
    i = uuid4().int
    wfst.s[i] = State(a=[], w=w)
    return i

def set_finalweight(wfst, i, w):
    wfst.s[i] = State(a=wfst.s[i].a, w=w)

def new_with_start(wfst, i):
    s = wfst.s[i] #check
    return Wfst(s0=i, s=wfst.s)

    
if __name__ == "__main__":
    wfst = Wfst(s0=None, s={})
    s0 = add_state(wfst)
    s1 = add_state(wfst)
    s2 = add_state(wfst)
    wfst.s[s0].a.append(Arc(i="a", o="a", w=0.5, n=s1))
    wfst = new_with_start(wfst, s0)

    from pprint import pprint
    pprint(wfst._asdict())
