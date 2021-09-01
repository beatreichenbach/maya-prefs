# Cuts and unwraps objects based on hard edges.

from maya import cmds
import maya.mel as mel


def cut_hard_edges():
    selection = cmds.ls(selection=True)
    if not selection:
        return
    for s in selection:
        cmds.select('{}.f[0:{}]'.format(s, cmds.polyEvaluate(s, f=True)))
        cmds.polyProjection(type='planar', insertBeforeDeformers=False, mapDirection='y')
        cmds.selectType(pe=True)
        cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
        cmds.polyMapCut()
        cmds.polySelectConstraint(sm=0)
        cmds.select('{}.map[0:{}]'.format(s, cmds.polyEvaluate(s, uv=True)))
        mel.eval('u3dUnfold -iterations 1 -pack 1 -borderintersection 1 -triangleflip 1 -mapsize 1024 -roomspace 2')
    cmds.select(s)
