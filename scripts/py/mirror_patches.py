# Mirrors the patches of selected UVs or all UVs on selected objects. Good with multiple UDIMs.

from maya import cmds
import re


def mirror_patches():
    objects = cmds.ls(selection=True, type='transform')
    for object in objects:
        mirror_uvs(object, range(cmds.polyEvaluate(object, uv=True)))
    
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
        mirror_uvs(object, uvs)


def mirror_uvs(object, uvs):
    for uv in uvs:
        uv = '{}.map[{}]'.format(object, uv)
        coord = cmds.polyEditUV(uv, query=True)
        pivot = [int(coord[0]/1) + .5, int(coord[1]/1) + .5]
        cmds.polyEditUV(uv, pu=pivot[0], pv=pivot[1], su=-1, sv=1)
