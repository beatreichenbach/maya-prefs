# Combines selected objects without destroying hierarchy and transforms.


from maya import cmds
from undo import undo


@undo
def combine():
    selection = cmds.ls(selection=True)
    first = selection[0]

    # get data
    parent = cmds.listRelatives(first, path=True, parent=True)
    position = cmds.xform(first, worldSpace=True, translation=True, q=True)
    rotation = cmds.xform(first, worldSpace=True, rotation=True, q=True)

    # create group so parent doesn't get deleted
    group = cmds.group(empty=True)
    cmds.xform(group, worldSpace=True, translation=position, rotation=rotation)
    if parent:
        cmds.parent(group, parent)

    # combine objects
    combined = cmds.polyUnite(selection, ch=False, name=first.rsplit('|', 1)[-1])
    combined = cmds.parent(combined, group)
    cmds.xform(combined, pivots=position, worldSpace=True)
    cmds.makeIdentity(combined, translate=True, rotate=True, apply=True)

    # reparent and delete group
    if parent:
        cmds.parent(combined, parent[0])
    else:
        cmds.parent(combined, world=True)
    cmds.delete(group)
