#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementation of a Weighted Finite State Transducer

"""
from typing import Optional
from uuid import uuid4 
from collections import namedtuple


#SEMIRING
class TropicalWeight(object):
    def __init__(self, value: Optional[float]=None):
        self._value = value

    @classmethod
    def zero(cls):
        return cls(float("inf"))

    @classmethod
    def one(cls):
        return cls(float(0.0))

    @classmethod
    def one(cls):
        return cls(float(0.0))

    @classmethod
    def from_str(cls, value: str):
        if value == "":
            return cls(None)
        else:
            return cls(float(value))
    
    def __add__(self, other: "TropicalWeight"):
        return TropicalWeight(min(self._value, other._value))

    def __mul__(self, other: "TropicalWeight"):
        return TropicalWeight(self._value + other._value)

    def __lt__(self, other: "TropicalWeight"):
        if other._value is None:
            return True
        elif self._value is None:
            return False
        return self._value < other._value

    def __eq__(self, other: "TropicalWeight"):
        return self._value == other._value
    
    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._value)


Arc = namedtuple("Arc", ["ilabel", "olabel", "weight", "next_state"])
State = namedtuple("State", ["arcs", "weight"])


class Wfst(object):
    """Note: Weight instances are not checked against semiring
    """
    def __init__(self, semiring=TropicalWeight):
        self._start = None
        self._states = {}
        self.W = semiring

    def __str__(self):
        pass
        
    @classmethod
    def from_spec(cls, semiring, start, states, final_states, arcs):
        wfst = cls(semiring)
        for state in states:
            if state in final_states:
                wfst.add_state(weight=final_states[state],
                               with_id=state)
            else:
                wfst.add_state(with_id=state)
        wfst.set_start(start)
        for arc in arcs:
            wfst.add_arc(state=arc[0], next_state=arc[1],
                         ilabel=arc[2], olabel=arc[3], weight=arc[4])
        return wfst

    def to_fsm_format(self):
        raise NotImplementedError

    def states(self):
        return self._states.keys().__iter__()

    def arcs(self, state):
        return self._states[state].arcs.__iter__()
    
    def add_state(self, weight=None, with_id=None):
        if with_id is None:
            i = uuid4().int
        else:
            i = with_id
        if weight is None:
            weight = self.W.zero()
        self._states[i] = State(arcs=[], weight=weight)
        return i

    def add_arc(self, state, next_state, ilabel, olabel, weight):
        self._states[state].arcs.append(Arc(ilabel=ilabel,
                                           olabel=olabel,
                                           weight=weight,
                                           next_state=next_state))

    def set_start(self, state):
        assert state in self._states
        self._start = state

    def get_start(self):
        return self._start

    def set_finalweight(self, state, weight):
        self._states[state] = State(arcs=self._states[state].arcs, weight=weight)

    def get_finalweight(self, state):
        return self._states[state].weight

    def is_final(self, state):
        return self._states[state].weight != self.W.zero()
