'''
  Author: Beat Reichenbach
  Date: 7/19/2015
  Version: 1.0

  Description: Mirrors the patches of selected UVs or all UVs on selected objects. Good with multiple UDIMs.

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_mirrorPatches
br_mirrorPatches.mirrorPatches()

'''

from maya import cmds
import re

def mirrorPatches():
    objects = cmds.ls(selection=True, type='transform')
    for object in objects:
        mirrorUVs(object, range(cmds.polyEvaluate(object, uv=True)))
    
    maps = cmds.ls(selection=True, type='float2')
    if not maps:
        return
    object = maps[0].split('.')[0]
    uvs = []
    for map in maps:
        uvRangeResult = re.search(r'\.map\[(\d+)(?::(\d+))?\]', map)
        if uvRangeResult:
            if uvRangeResult.group(2):
                uvs.extend(range(int(uvRangeResult.group(1)), int(uvRangeResult.group(2)) + 1))
            else:
                uvs.append(uvRangeResult.group(1))
    if uvs:
        mirrorUVs(object, uvs)
        
def mirrorUVs(object, uvs):
    for uv in uvs:
        uv = '{}.map[{}]'.format(object, uv)
        coord = cmds.polyEditUV(uv, query=True)
        pivot = [int(coord[0]/1) + .5, int(coord[1]/1) + .5]
        cmds.polyEditUV(uv, pu=pivot[0], pv=pivot[1], su=-1, sv=1)