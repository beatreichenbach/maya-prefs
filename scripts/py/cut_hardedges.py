'''
  Author: Beat Reichenbach
  Date: 2/3/2017
  Version: 1.1

  Description: Cuts and unwraps objects based on hard edges

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
                
IMPORTANT: For Maya 2017+ replace line 32 with:
        mel.eval('u3dUnfold -iterations 1 -pack 1 -borderintersection 1 -triangleflip 1 -mapsize 1024 -roomspace 2')


import br_cutHardEdges
br_cutHardEdges.cutHardEdges()

'''

from maya import cmds
import maya.mel as mel

def cutHardEdges():
    for s in cmds.ls(selection=True):
        cmds.select('{}.f[0:{}]'.format(s, cmds.polyEvaluate(s, f=True)))
        cmds.polyProjection(type='planar', insertBeforeDeformers=False, mapDirection='y')
        cmds.selectType(pe=True)
        cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
        cmds.polyMapCut()
        cmds.polySelectConstraint( sm=0 )
        cmds.select('{}.map[0:{}]'.format(s, cmds.polyEvaluate(s, uv=True)))
        mel.eval('u3dUnfold -iterations 1 -pack 1 -borderintersection 1 -triangleflip 1 -mapsize 1024 -roomspace 2')
    cmds.select(s)