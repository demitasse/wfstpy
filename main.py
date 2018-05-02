#!/usr/bin/env python3
"""Simple demonstration script
"""

from wfst import *
from algo import extendfinal


def to_string(wfst):
    lines = []
    for s in wfst.st:
        lines.append(" ".join(map(str, [s, wfst.st[s].wt])))
        for a in wfst.st[s].ar:
            lines.append("\t" + " ".join(map(str, a)))
    return "\n".join(lines)


if __name__ == "__main__":
    wfst = new_wfst()
    #add states
    states = []
    for i in range(3):
        states.append(add_state(wfst))
    set_finalweight(wfst, states[-1], 3.5)
    #add arcs
    wfst.st[states[0]].ar.append(Arc(il="a", ol="x", wt=0.5, nst=states[1]))
    wfst.st[states[0]].ar.append(Arc(il="b", ol="y", wt=1.5, nst=states[1]))
    wfst.st[states[1]].ar.append(Arc(il="c", ol="z", wt=2.5, nst=states[2]))
    #set starting state
    wfst = make_with_start(wfst, states[0])


    print(to_string(wfst))
    print()
    extendfinal(wfst)
    print(to_string(wfst))
