# Extract the currently selected faces from the object without separating different shells. Slow!

from maya import cmds, mel

def extract_faces():
    faces = cmds.filterExpand(selectionMask=34, expand=False, fullPath=False) # Polygon Face
    if not faces:
        cmds.error("No faces selected.")

    shapes = set(cmds.listRelatives(faces, parent=True, fullPath=True))
    objects = cmds.listRelatives(shapes, parent=True, fullPath=True)

    # duplicate objects and remove any children
    duplicates = []
    for object in objects:
        duplicate = cmds.duplicate(object)[0]
        duplicates.append(duplicate)

        children = cmds.listRelatives(duplicate, children=True, type='transform', fullPath=True)
        if children:
            cmds.delete(children)

    # get selected faces on duplicates
    cmds.select(duplicates)
    mel.eval('changeSelectMode -component;')
    duplicateFaces = cmds.filterExpand(selectionMask=34, expand=False, fullPath=False) # Polygon Face

    # invert selection on duplicates
    cmds.select(clear=True)
    for object in duplicates:
        cmds.select('{}.f[*]'.format(object), add=True)
    cmds.select(duplicateFaces, deselect=True)
    cmds.delete()

    # delete original selection
    cmds.delete(faces)

    cmds.select(duplicates, replace=True)
