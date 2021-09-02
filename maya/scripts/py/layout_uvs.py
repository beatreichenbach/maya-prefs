# Layout uvs grouped by objects and gap in between.
#
# Args:
#     gap (float): Gap between each group of uvs in uvspace.

from maya import cmds


def layout_uvs(gap=0.05):
    previous = (0, 0)
    objects = cmds.ls(selection=True)
    for obj in objects:
        boundingBox = cmds.polyEvaluate(obj, boundingBox2d=True)
        cmds.select('{}.map[0:{}]'.format(obj, cmds.polyEvaluate(obj, uv=True)), replace=True)
        offsetX = - boundingBox[0][0] + previous[0] + gap
        offsetY = - boundingBox[1][0] + gap
        cmds.polyEditUV(u=offsetX, v=offsetY)
        previous = (offsetX + boundingBox[0][1], offsetY + boundingBox[1][1])
    cmds.select(objects, replace=True)
    
