'''
  Author: Beat Reichenbach
  Date: 07/09/2017
  Version: 1.0

  Description: Transfer Shaders from one object to another

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.

import br_transferShaders
br_transferShaders.ui()


'''

from maya import cmds

import re
import json
import os

window = 'transferShadersWindow'
filepath = os.path.join(cmds.workspace(rootDirectory=True, query=True), 'shaders.mb')

def ui():
    if cmds.window(window, exists=True):
        deleteWindow()
    if cmds.windowPref(window, exists=True):
        cmds.windowPref(window, remove=True)

    cmds.window(window, title='Transfer Shaders', widthHeight=(200, 100), sizeable=False)
    form = cmds.formLayout()

    commands = [
    ['Import Selected', 'importSelected()'],
    ['Export Selected', 'exportSelected()'],

    ['Close', 'deleteWindow()'],
    ]

    buttons = [cmds.button(label=command[0], width=160, command='br_transferShaders.{}'.format(command[1])) for command in commands]

    cmds.window(window, edit=True, widthHeight=(200, (len(buttons)*40 + 20)))

    for i, button in enumerate(buttons):
        cmds.formLayout(form, edit=True, attachForm=[(button, 'left', 20), (button, 'top', i*40 + 20)])
    cmds.showWindow(window)

def deleteWindow():
    cmds.deleteUI(window)

def exportSelected():
    namespaceRE = re.compile(r'(^|\|)(\w+):')

    assignments = {}
    shadingGroups = set()

    selection = cmds.ls(selection=True, long=True)

    for node in selection:
        shapes = cmds.listRelatives(cmds.ls(selection=True), allDescendents=True, type='mesh', fullPath=True) or []

        for shape in shapes:
            shadingGroup = cmds.listSets(extendToShape=True, type=1, object=shape)[0]
            shadingGroups.add(shadingGroup)
            shadingGroup = namespaceRE.sub('', shadingGroup)
            shapeList = assignments.get(shadingGroup, [])
            shape = namespaceRE.sub('|', shape)
            shapeList.append(shape)
            assignments[shadingGroup] = shapeList

    # cmds.fileInfo('assignments', json.dumps(assignments))
    try:
        dataNode = cmds.scriptNode(name='shaders')
        cmds.addAttr(dataNode, longName='assignments', dataType='string')
        cmds.setAttr('{}.assignments'.format(dataNode), json.dumps(assignments), type='string')

        selection = list(shadingGroups) + ['shaders']
        print selection
        cmds.select(selection, replace=True, noExpand=True)
        cmds.file(filepath, force=True, type='mayaBinary', exportSelected=True)
        print filepath
    except Exception as e:
        print cmds.error(e)
    finally:
        cmds.delete(dataNode)

def importSelected():
    cmds.file(filepath, i=True, ignoreVersion=True, preserveReferences=True, mergeNamespacesOnClash=True)

    selection = cmds.ls(selection=True, long=True)
    if cmds.objExists('shaders'):
        try:
            data = cmds.getAttr('shaders.assignments')
            assignments = json.loads(data)

            # for node in selection:
            #     if ':' in node:
            #         namespace, name = node.rsplit(':', 1)

            for shadingGroup, shapes in assignments.iteritems():
                shapes = filter(lambda node: cmds.objExists(node), shapes)
                cmds.sets(shapes, edit=True, forceElement=shadingGroup)
        finally:
            cmds.delete('shaders')
            os.remove(filepath)

