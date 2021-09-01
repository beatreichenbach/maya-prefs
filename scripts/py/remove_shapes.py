# Removes any additional shape nodes if an object has more than one.

from maya import cmds


def remove_shapes():
    for s in cmds.ls(selection=True):
        shapes = cmds.listRelatives(s, shapes=True, fullPath=True)
        if shapes and len(shapes) > 1:
            for shape in shapes[1:]:
                cmds.delete(shape)
            cmds.inViewMessage(
                statusMessage='Removed {} shapes from {}'.format(len(shapes) - 1, s),
                pos='topCenter',
                fade=True)
