# Unwrap them cube like objects by cutting all edges on one face and then unwrapping it like a box.
# It will try to keep always one edge connected so it creates only one shell.

from maya import cmds
from maya import mel
import re

window = 'cube_unwrap_window'


def select_by_normal(object, vector):
    normals = cmds.polyInfo(object, faceNormals=True)
    faces = []
    for i in range(cmds.polyEvaluate(object, f=True)):
        normal = [float(normals[i].rsplit(' ', 3)[j]) for j in range(-3, 0)]
        dotProduct = sum(p * q for p, q in zip(normal, vector))
        if dotProduct + .5 > 1:
            faces.append(i)
    return faces    


def select_components(object, indices, type='f'):
    components = ('f', 'e', 'vtx')
    if type in components:
        for i in indices:
            cmds.select('{}.{}[{}]'.format(object, type, i), add=True)


def get_indices(selection):
    indices = []
    for s in selection:
        result = re.search(r'\[(\d+)(?::(\d+))?\]', s) 
        if result and result.group(2):
            indices.extend(range(int(result.group(1)), int(result.group(2)) + 1))
        elif result:
            indices.append(int(result.group(1)))
    return indices


def unwrap(axis=0):
    directions = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))
    axis = cmds.radioButtonGrp('axis_radio', query=True, select=True) - 1
    if axis == -1:
        axis = cmds.radioButtonGrp('axis_radio_2', query=True, select=True) + 2
    frontDirection = directions[axis]

    for object in cmds.ls(selection=True):
        backDirection = tuple([-i for i in frontDirection])
        
        sideDirections = list(directions)
        sideDirections.remove(frontDirection)
        sideDirections.remove(backDirection)
        
        sideEdges = []
        for d in sideDirections:
            cmds.select(clear=True)
            select_components(object, select_by_normal(object, d), type='f')

            edges = cmds.polyListComponentConversion(
                cmds.ls(selection=True),
                fromFace=True,
                toEdge=True,
                border=True)
            sideEdges.extend(get_indices(edges))
        
        cutEdges = [s for s in sideEdges if sideEdges.count(s) > 1]
        
        backEdges = []
        for d in (backDirection, sideDirections[0]):
            cmds.select(clear=True)
            select_components(object, select_by_normal(object, d), type='f')
            edges = cmds.polyListComponentConversion(
                cmds.ls(selection=True),
                fromFace=True,
                toEdge=True,
                border=True)
            backEdges.append(get_indices(edges))
        
        backEdges = set(backEdges[0]) - set(backEdges[1])
        
        cutEdges.extend(backEdges)
        
        cmds.select(object + '.e[:]', replace=True)
        cmds.polyMapSewMove()
        
        cmds.select(clear=True)
        select_components(object, cutEdges, type='e')
        cmds.polyMapCut()
        
        cmds.select(object + '.map[:]', replace=True)
        
        mel.eval('u3dUnfold -iterations 1 -pack 1 -borderintersection 1 -triangleflip 1 -mapsize 1024 -roomspace 2')
        cmds.delete(object, constructionHistory=True)
        cmds.select(object, replace=True)
        
 
def delete_window():
    cmds.deleteUI(window)


def ui():
    if cmds.window(window, exists=True):
        delete_window()
    if cmds.windowPref(window, exists=True):
        cmds.windowPref(window, remove=True)
    
    cmds.window(window, title='Unwrap Cubes', widthHeight=(550, 120), sizeable=False)
    form = cmds.formLayout()
    frame = cmds.frameLayout(borderVisible=True, labelVisible=False, width=530, height=70)
    cmds.formLayout(form, edit=True, attachForm=[(frame, 'left', 10), (frame, 'top', 10)])
    
    settings_form = cmds.formLayout()
    axis_radio = cmds.radioButtonGrp('axis_radio', label='Axis:', labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3)
    axis_radio_2 = cmds.radioButtonGrp('axis_radio_2', numberOfRadioButtons=3, shareCollection=axis_radio, label='', labelArray3=['-X', '-Y', '-Z'] )
    cmds.radioButtonGrp(axis_radio, edit=True, select=0)
    cmds.formLayout(settings_form, edit=True, attachForm=[(axis_radio, 'left', -50), (axis_radio, 'top', 10)])
    cmds.formLayout(settings_form, edit=True, attachForm=[(axis_radio_2, 'left', -50), (axis_radio_2, 'top', 40)])
    
    cmds.setParent(form)
    buttons = []
    buttons.append(cmds.button(label='Unwrap', width=170, command='cube_unwrap.unwrap(); cube_unwrap.delete_window();'))
    buttons.append(cmds.button(label='Apply', width=170, command='cube_unwrap.unwrap()'))
    buttons.append(cmds.button(label='Close', width=170, command='cube_unwrap.delete_window()'))
    cmds.formLayout(form, edit=True, attachForm=[(buttons[0], 'left', 10), (buttons[0], 'top', 90)])
    cmds.formLayout(form, edit=True, attachForm=[(buttons[1], 'left', 190), (buttons[1], 'top', 90)])
    cmds.formLayout(form, edit=True, attachForm=[(buttons[2], 'left', 370), (buttons[2], 'top', 90)])
    cmds.showWindow(window)
