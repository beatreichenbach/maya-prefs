'''
  Author: Beat Reichenbach
  Date: 10/09/2015
  Version: 1.1

  Description: Different small functions for production
  
  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_functions
br_functions.ui()

or run the scripts on their own, a few examples below:

import br_functions
br_functions.mergeVertices(0.01)

import br_functions
br_functions.toggleVertBoundary()

import br_functions
br_functions.createCamera()


'''

from maya import cmds
import random as rand
from maya import mel

window = 'functionsWindow'

def ui():
    if cmds.window(window, exists=True):
        deleteWindow()
    if cmds.windowPref(window, exists=True):
        cmds.windowPref(window, remove=True)
    
    cmds.window(window, title='Tools', widthHeight=(200, 100), sizeable=False)
    form = cmds.formLayout()
    
    commands = [
    ['Select Random', 'selectRandom()'],
    ['Rename Pasted', 'renamePasted()'],
    ['Remove Shapes', 'removeShapes()'],
    ['Merge Vertices', 'mergeVertices(0.01)'],
    ['Create Camera', 'createCamera()'],
    ['Open spPaint3D', 'spPaint()'],
    
    ['Close', 'deleteWindow()'],
    ]
    
    buttons = [cmds.button(label=command[0], width=160, command='br_functions.{}'.format(command[1])) for command in commands]
    
    cmds.window(window, edit=True, widthHeight=(200, (len(buttons)*40 + 20)))
    
    for i, button in enumerate(buttons):
        cmds.formLayout(form, edit=True, attachForm=[(button, 'left', 20), (button, 'top', i*40 + 20)])
    cmds.showWindow(window)
    
def deleteWindow():
    cmds.deleteUI(window)

def mergeVertices(threshold):
    selection = cmds.ls(selection=True)
    for s in selection:
        n = cmds.polyEvaluate(s, vertex=True)
        cmds.polyMergeVertex(s, distance=threshold)
        merged = (n - cmds.polyEvaluate(s, vertex=True))
        cmds.inViewMessage( statusMessage='{} Vertice{} merged'.format(merged, 's'[merged==1:]), pos='topCenter', fade=True )

def selectRandom():
    randSel = []
    for s in cmds.ls(selection=True):
        if rand.getrandbits(1):
            randSel.append(s)
    cmds.select(randSel)
            
def renamePasted():
    for s in reversed(cmds.ls(selection=True)):
        nodes = cmds.listRelatives(s, allDescendents=True, type='transform', fullPath=True)
        if not nodes:
            nodes = []
        nodes.append(s)
        for n in nodes:
            name = n.rsplit('|',1)[-1]
            cmds.rename(n, name.replace('pasted__',''))

def removeShapes():
    for s in cmds.ls(selection=True):
        shapes = cmds.listRelatives(s, shapes=True, fullPath=True)
        if shapes and len(shapes) > 1:
            i = 0
            for shape in shapes[1:]:
                cmds.delete(shape)
                i += 1
            print 'Removed {} shapes from {}'.format(i, s)
        
def spPaint():
    import spPaint3dGui
    spPaint3dwin=spPaint3dGui.spPaint3dWin()
    
def createCamera(name='shotCam'):
    sourceCam = cmds.modelPanel(cmds.getPanel(withFocus=True), q=True, camera=True)
    cam = cmds.camera()[0]
    cam = cmds.rename(cam, name)
    ratio = cmds.getAttr('defaultResolution.deviceAspectRatio')
    camShape = cmds.listRelatives(cam, s=True)[0]
    cmds.setAttr(camShape+".focalLength", 50)
    cmds.setAttr(camShape+".horizontalFilmAperture", ratio)
    cmds.setAttr(camShape+".locatorScale", 10)
    cmds.xform(cam, ws=True, t=cmds.xform(sourceCam, ws=True, t=True, q=True), ro=cmds.xform(sourceCam, ws=True, ro=True, q=True))