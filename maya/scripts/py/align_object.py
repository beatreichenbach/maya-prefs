# Select 2 or 3 vertices on an object to align the axis to those.
# Select three vertices A, B, (C) that form a right angle in the following order:
# .A .B
# .C


from maya import cmds

class Isolate():
    def __init__(self, object):
        self.object = object

    def __enter__(self):
        self.parents = cmds.listRelatives(self.object, parent=True, type='transform', path=True)
        self.children = cmds.listRelatives(self.object, children=True, type='transform', path=True)

        if self.children:
            self.child_group = cmds.group(empty=True)
            self.children = cmds.parent(self.children, self.child_group)

        return self.object

    def __exit__(self, type, value, traceback):
        if self.parents:
            self.object = cmds.parent(self.object, self.parents[0])
        else:
            self.object = cmds.parent(self.object, w=True)
        if self.children:
            cmds.parent(self.children, self.object)
            cmds.delete(self.child_group)

def align_object():
    selection = cmds.ls(selection=True, flatten=True)
    vertices = [vertex for vertex in selection if '.vtx[' in vertex]
    locators = []

    if not vertices:
        return

    object = vertices[0].split('.')[0]

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

    with Isolate(object) as i:
        cmds.parent(object, locators[0])
        cmds.makeIdentity(apply=True, rotate=True)

    cmds.delete(locators)
