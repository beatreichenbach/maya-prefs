'''
  Author: Beat Reichenbach
  Date: 10/09/2015
  Version: 1.1

  Description: Different small functions for production

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.

import br_functions
br_functions.mergeVertices(0.01)


'''

from maya import cmds

def mergeVertices(threshold):
    selection = cmds.ls(selection=True)
    for s in selection:
        n = cmds.polyEvaluate(s, vertex=True)
        cmds.polyMergeVertex(s, distance=threshold)
        merged = (n - cmds.polyEvaluate(s, vertex=True))
        cmds.inViewMessage( statusMessage='{} Vertice{} merged'.format(merged, 's'[merged==1:]), pos='topCenter', fade=True )
