'''
  Author: Beat Reichenbach
  Date: 10/05/2015
  Version: 1.0

  Description: Moves the selected object to the last selected objects position.

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.

import br_copyTransform
br_copyTransform.copyTransform()

'''

from maya import cmds


def copyTransform():
    objects = cmds.ls(sl=True, type='transform')
    target = cmds.ls(sl=True, tail=True)
    objects.remove(target[0])

    pos = cmds.xform(target, translation=True, worldSpace=True, query=True)
    rot = cmds.xform(target, rotation=True, worldSpace=True, query=True)

    for o in objects:
        cmds.xform(o, translation=pos, rotation=rot, worldSpace=True)
    cmds.select(objects)
