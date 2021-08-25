'''
  Author: Beat Reichenbach
  Date: 10/09/2015
  Version: 1.0

  Description: Unwraps the whole objects with Unfold 3d instead of having to select UVs
  
  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
                
IMPORTANT: For Maya 2017+ replace line 26 with:
        mel.eval('u3dUnfold -iterations 1 -pack 1 -borderintersection 1 -triangleflip 1 -mapsize 1024 -roomspace 2')
  
import br_unwrapObjects
br_unwrapObjects.unwrapObjects()

'''

from maya import cmds
from maya import mel

def unwrapObjects():
    for s in cmds.ls(selection=True):
        split = s.split('.')
        if len(split) > 1:
            s = split[0]
        cmds.select('{}.map[0:{}]'.format(s, cmds.polyEvaluate(s, uv=True)), replace=True)
        mel.eval('u3dUnfold -iterations 1 -pack 1 -borderintersection 1 -triangleflip 1 -mapsize 1024 -roomspace 2')
        if len(split) > 1:
            break
    cmds.select(s)