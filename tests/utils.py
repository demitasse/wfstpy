from copy import deepcopy


def walk_all(wfst, remove_epsilon=True):
    """Walk all paths (depth-first) and return input label sequences and
       path weights. Obviously if the WFST contains cycles this will
       not return.

    """
    s = wfst.get_start()
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
    for arc in wfst.arcs(state):
        current[0].append((arc.ilabel, arc.olabel))
        current[1] *= arc.weight
        if wfst.is_final(arc.next_state):
            current[1] *= wfst.get_finalweight(arc.next_state)
            paths.append(current)
        else:
            _dfs_next(wfst, arc.next_state, deepcopy(current), paths)
