# Create duplicate mesh and apply subdivisions with all settings.

from maya import cmds


def poly_smooth():
    for obj in cmds.ls(selection=True):
        shapes = cmds.listRelatives(obj, shapes=True)
        if not shapes:
            continue
             
        shape = shapes[0]
        smooth_level = cmds.getAttr('{}.smoothLevel'.format(shape))
        ofb = cmds.getAttr('{}.osdFvarBoundary'.format(shape))
        ovb = cmds.getAttr('{}.osdVertBoundary'.format(shape))
        ofc = cmds.getAttr('{}.osdFvarPropagateCorners'.format(shape))
        shape_smooth = cmds.duplicate(shape)
        cmds.polySmooth(
            shape_smooth,
            method=0,
            subdivisionType=2,
            osdVertBoundary=ovb,
            osdFvarBoundary=ofb,
            osdFvarPropagateCorners=ofc,
            osdSmoothTriangles=0,
            osdCreaseMethod=0,
            divisions=smooth_level)
        cmds.select(shape_smooth)
