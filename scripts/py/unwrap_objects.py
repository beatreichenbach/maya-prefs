# Unwraps the whole objects with Unfold 3d instead of having to select UVs.

from maya import cmds
from maya import mel


def unwrap_objects():
    selection = cmds.ls(selection=True)
    if not selection:
        return
    for s in selection:
        split = s.split('.')
        if len(split) > 1:
            s = split[0]
        cmds.select('{}.map[0:{}]'.format(s, cmds.polyEvaluate(s, uv=True)), replace=True)
        mel.eval('u3dUnfold -iterations 1 -pack 1 -borderintersection 1 -triangleflip 1 -mapsize 1024 -roomspace 2')
        if len(split) > 1:
            break
    cmds.select(s)
