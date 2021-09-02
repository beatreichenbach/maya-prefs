# Moves the selected object to the last selected object's position.

from maya import cmds


def copy_transform():
    objects = cmds.ls(sl=True, type='transform')
    target = cmds.ls(sl=True, tail=True)
    objects.remove(target[0])

    pos = cmds.xform(target, translation=True, worldSpace=True, query=True)
    rot = cmds.xform(target, rotation=True, worldSpace=True, query=True)

    for o in objects:
        cmds.xform(o, translation=pos, rotation=rot, worldSpace=True)
    cmds.select(objects)
