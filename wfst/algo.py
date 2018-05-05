#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple implementations of WFST algorithms

"""
from collections import namedtuple

from . import *

def extendfinal(wfst):
    """Modifies the input...
    """
    final_states = [s for s in wfst.st if is_final(wfst, s)]
    new_final = add_state(wfst, wfst.sr.one)
    #connect finals to new final
    for s in final_states:
        wt = wfst.st[s].wt
        wfst.st[s].ar.append(Arc(il=None, ol=None, wt=wt, nst=new_final))
        wfst.st[s] = State(ar=wfst.st[s].ar, wt=wfst.sr.zero)
