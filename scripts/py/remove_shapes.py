'''
  Author: Beat Reichenbach
  Date: 10/09/2015
  Version: 1.1

  Description: Different small functions for production

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.

import br_removeShapes
br_removeShapes.removeShapes()


'''

from maya import cmds

def removeShapes():
    for s in cmds.ls(selection=True):
        shapes = cmds.listRelatives(s, shapes=True, fullPath=True)
        if shapes and len(shapes) > 1:
            i = 0
            for shape in shapes[1:]:
                cmds.delete(shape)
                i += 1
            cmds.inViewMessage( statusMessage='Removed {} shapes from {}'.format(i, s), pos='topCenter', fade=True )
