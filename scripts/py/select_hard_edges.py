# Select hard edges.

from maya import cmds


def select_hard_edges():
    cmds.selectType(pe=True)
    cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
    edges = cmds.ls(selection=True)
    cmds.polySelectConstraint(sm=0)
    cmds.select(edges)
    cmds.polySelectConstraint(disable=True)
