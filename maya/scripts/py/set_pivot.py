# Sets the translate pivot to the rotate/scale pivot.

from maya import cmds


def set_pivot():
    selection = cmds.ls(selection=True, type='transform')
    for s in selection:
        parents = cmds.listRelatives(s, parent=True, type='transform', path=True)
        children = cmds.listRelatives(s, children=True, type='transform', path=True)
        pos = cmds.xform(s, rotatePivot=True, worldSpace=True, query=True)
        tempGrp = cmds.group(empty=True)
        if children:
            childGrp = cmds.group(empty=True)
            children = cmds.parent(children, childGrp)
        cmds.xform(tempGrp, t=pos)
        s = cmds.parent(s, tempGrp)
        cmds.makeIdentity(s, apply=True, t=True)
        if parents:
            s = cmds.parent(s, parents[0])
        else:
            s = cmds.parent(s, w=True)
        if children:
            cmds.parent(children, s)
            cmds.delete(childGrp)     
        cmds.delete(tempGrp)
    cmds.select(selection, replace=True)
