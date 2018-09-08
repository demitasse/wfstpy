from copy import deepcopy

from wfst import get_finalweight, is_final

def walk_all(wfst, remove_epsilon=True):
    """Walk all paths (depth-first) and return input label sequences and
       path weights. Obviously if the WFST contains cycles this will
       not return.

    """
    s = wfst.st0
    paths = []
    curr = [[], wfst.W.one()]
    _dfs_next(wfst, s, curr, paths)
    if remove_epsilon:
        for path in paths:
            path[0] = [e for e in path[0] if e != (None, None)]
    for path in paths:
        path[0] = " ".join([":".join(map(str, e)) for e in path[0]])
    return paths

def _dfs_next(wfst, state, current, paths):
    for arc in wfst.st[state].ar:
        current[0].append((arc.il, arc.ol))
        current[1] *= arc.wt
        if is_final(wfst, arc.nst):
            current[1] *= get_finalweight(wfst, arc.nst)
            paths.append(current)
        else:
            _dfs_next(wfst, arc.nst, deepcopy(current), paths)
