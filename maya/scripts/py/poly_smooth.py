# Create duplicate mesh and apply subdivisions with all settings.

from maya import cmds


def poly_smooth(objects):
    if not objects:
        objects = cmds.ls(selection=True, long=True)
        objects = cmds.listRelatives(objects, allDescendents=True, fullPath=True, type='transform')
    elif not isinstance(objects, list):
        objects = [objects]

    for obj in objects:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if not shapes:
            continue
        shape = shapes[0]

        smooth_level = cmds.getAttr('{}.smoothLevel'.format(shape))
        ofb = cmds.getAttr('{}.osdFvarBoundary'.format(shape))
        ovb = cmds.getAttr('{}.osdVertBoundary'.format(shape))
        ofc = cmds.getAttr('{}.osdFvarPropagateCorners'.format(shape))
        if smooth_level:
            cmds.polySmooth(
                shape,
                method=0,
                subdivisionType=2,
                osdVertBoundary=ovb,
                osdFvarBoundary=ofb,
                osdFvarPropagateCorners=ofc,
                osdSmoothTriangles=0,
                osdCreaseMethod=0,
                divisions=smooth_level)
