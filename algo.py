#!/usr/bin/env python3
"""Simple implementations of WFST algorithms

"""
from collections import namedtuple

from wfst import *

def extendfinal(wfst):
    final_states = [s for s in wfst.st if is_final(wfst, s)]
    new_final = add_state(wfst, wfst.sr.one)
    #connect finals to new final
    for s in final_states:
        #print(s)
        wt = wfst.st[s].wt
        wfst.st[s].ar.append(Arc(il=None, ol=None, wt=wt, nst=new_final))
        wfst.st[s] = State(ar=wfst.st[s].ar, wt=wfst.sr.zero)
