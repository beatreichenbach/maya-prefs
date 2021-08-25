'''
  Author: Beat Reichenbach
  Date: 05/29/2017
  Version: 1.0

  Description: Moves the selected object to the last selected objects position.

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_insertRemap
br_insertRemap.insertRemap()

'''
from maya import cmds

def insertRemap():
    selection = cmds.ls(selection=True)[0]

    remap = cmds.shadingNode('remapValue', asUtility=True)
    cmds.setAttr(remap + '.value[0].value_Interp', 3)
    cmds.setAttr(remap + '.value[1].value_Interp', 3)

    if cmds.connectionInfo(selection + '.outColor', isSource=True):
        outPlug = cmds.connectionInfo(selection + '.outColor', destinationFromSource=True)[0]
        cmds.connectAttr(selection + '.outColorR', remap + '.inputValue')
        for c in ('R', 'G', 'B'):
            cmds.connectAttr(remap + '.outValue', outPlug + c, force=True)    
        cmds.disconnectAttr(selection + '.outColor', outPlug)

    elif cmds.connectionInfo(selection + '.outAlpha', isSource=True):
        outPlug = cmds.connectionInfo(selection + '.outAlpha', destinationFromSource=True)[0]
        cmds.connectAttr(selection + '.outAlpha', remap + '.inputValue')
        cmds.connectAttr(remap + '.outValue', outPlug, force=True)