#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementation of a Weighted Finite State Transducer

"""
from uuid import uuid4 
from collections import namedtuple


##DEFS
Wfst = namedtuple("Wfst", "st0 st sr") #start, states, semiring
Arc = namedtuple("Arc", "il ol wt nst") #ilabel, olabel, weight, nextstate
State = namedtuple("State", "ar wt") #arcs, weight
Semiring = namedtuple("Semiring", "plus times zero one")

#SEMIRINGS
SR_TROPICAL = Semiring(plus=lambda x,y: min(x, y),
                       times=lambda x,y: x + y,
                       zero=float("inf"),
                       one=float(0.0))

##CONVENIENCE FUNCS
def add_state(wfst, weight=None):
    i = uuid4().int
    if weight is None:
        weight = wfst.sr.zero
    wfst.st[i] = State(ar=[], wt=weight)
    return i

def set_finalweight(wfst, state, weight):
    wfst.st[state] = State(ar=wfst.st[state].ar, wt=weight)

def new_wfst(semiring=SR_TROPICAL):
    return Wfst(st0=None, st={}, sr=semiring)

def make_with_start(wfst, i):
    s = wfst.st[i] #check
    return Wfst(st0=i, st=wfst.st, sr=wfst.sr)

def is_final(wfst, state):
    return wfst.st[state].wt != wfst.sr.zero
