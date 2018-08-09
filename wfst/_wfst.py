#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementation of a Weighted Finite State Transducer

"""
from typing import Optional
from uuid import uuid4 
from collections import namedtuple


##DEFS
Wfst = namedtuple("Wfst", "st0 st W") #start, states, Weight class (semiring)
Arc = namedtuple("Arc", "il ol wt nst") #ilabel, olabel, weight, nextstate
State = namedtuple("State", "ar wt") #arcs, weight
Semiring = namedtuple("Semiring", "plus times zero one")

#SEMIRINGS
class TropicalWeight(object):
    def __init__(self, value: Optional[float]=None):
        self.value = value

    @classmethod
    def zero(cls):
        return cls(float("inf"))

    @classmethod
    def one(cls):
        return cls(float(0.0))

    def __add__(self, other: "TropicalWeight"):
        return TropicalWeight(min(self.value, other.value))

    def __mul__(self, other: "TropicalWeight"):
        return TropicalWeight(self.value + other.value)

    def __lt__(self, other: "TropicalWeight"):
        if other.value is None:
            return True
        elif self.value is None:
            return False
        return self.value < other.value

    def __eq__(self, other: "TropicalWeight"):
        return self.value == other.value
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.value)
    


##CONVENIENCE FUNCS
def add_state(wfst, weight=None, with_id=None):
    if with_id is None:
        i = uuid4().int
    else:
        i = with_id
    if weight is None:
        weight = wfst.W.zero()
    wfst.st[i] = State(ar=[], wt=weight)
    return i

def set_finalweight(wfst, state, weight):
    wfst.st[state] = State(ar=wfst.st[state].ar, wt=weight)

def new_wfst(semiring=TropicalWeight):
    return Wfst(st0=None, st={}, W=TropicalWeight)

def make_with_start(wfst, state):
    s = wfst.st[state] #check
    return Wfst(st0=state, st=wfst.st, W=wfst.W)

def is_final(wfst, state):
    return wfst.st[state].wt != wfst.W.zero()
