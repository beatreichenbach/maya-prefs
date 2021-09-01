# Select every nth edge. Select two edges.
# It will complete the edge ring with every nth edge selected.

import re
from maya import cmds


def select_nth_edge():
    selection = "".join(cmds.ls(selection=True))
    indices = list(map(int, re.findall(r'\[([0-9]+)\]', selection)))
    if len(indices) >= 2:
        cmds.polySelect(rpt=indices[:2])
