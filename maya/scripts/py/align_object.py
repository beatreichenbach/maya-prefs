# Select 2 or 3 vertices on an object to align the axis to those.
# Select three vertices A, B, (C) that form a right angle in the following order:
# .A .B
# .C


from maya import cmds


def align_object():
    selection = cmds.ls(selection=True, flatten=True)
    vertices = [vertex for vertex in selection if '.vtx[' in vertex]
    locators = []

    if not vertices:
        return

    obj = vertices[0].split('.')[0]

    for vertex in vertices[:3]:
        position = cmds.xform(vertex, query=True, worldSpace=True, translation=True)
        locator = cmds.spaceLocator()
        cmds.xform(locator, worldSpace=True, translation=position)
        locators.extend(locator)

    if len(vertices) == 2:
        cmds.aimConstraint(
            locators[1], locators[0],
            offset=[0, 0, 0],
            aimVector=[1, 0, 0],
            upVector=[0, 1, 0],
            worldUpVector=[0, 1, 0],
            worldUpType='vector')

    if len(vertices) == 3:
        cmds.aimConstraint(
            locators[1], locators[0],
            offset=[0, 0, 0],
            aimVector=[1, 0, 0],
            upVector=[0, 1, 0],
            worldUpVector=[0, 1, 0],
            worldUpType='object',
            worldUpObject=locators[2])

    parents = cmds.listRelatives(obj, parent=True, type='transform', path=True)
    children = cmds.listRelatives(obj, children=True, type='transform', path=True)

    if children:
        child_group = cmds.group(empty=True)
        children = cmds.parent(children, child_group)

    obj = cmds.parent(obj, locators[0])
    cmds.makeIdentity(obj, apply=True, rotate=True)

    if parents:
        obj = cmds.parent(obj, parents[0])
    else:
        obj = cmds.parent(obj, world=True)
    if children:
        cmds.parent(children, obj)
        cmds.delete(child_group)

    cmds.delete(locators)
