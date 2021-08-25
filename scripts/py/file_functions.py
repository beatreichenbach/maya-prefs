'''
  Author: Beat Reichenbach
  Date: 9/1/2015
  Version: 1.0

  Description: Import multiplie files and delete the mtl file when importing obj. Export selected to a specified temp directory as obj.

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.

import br_fileFunctions
br_fileFunctions.importFiles()

'''

from maya import cmds
import os
import sys

lastImportPath = ''


def importFiles(deleteMaterial=True):
    try:
        importFiles.lastImportPath
        importPath = importFiles.lastImportPath
    except:
        importPath = cmds.workspace(query=True, rootDirectory=True)

    fileDialog = cmds.fileDialog2(caption='Import Objects', startingDirectory=importPath, fileMode=4, okCaption='Import')
    if not fileDialog:
        return
    for file in fileDialog:
        file = file.replace('\\', '/')
        filename, ext = os.path.basename(file).split('.')
        if 'mtl' == ext:
            continue

        if deleteMaterial:
            mtlFile = file.replace(ext, 'mtl')

            if os.path.isfile(mtlFile):
                os.remove(mtlFile)

        mesh = cmds.file(file, i=True, ignoreVersion=True, renameAll=True, preserveReferences=True, returnNewNodes=True)

        if len(mesh) > 0:
            cmds.rename(mesh[0], filename)

    importFiles.lastImportPath = file.rsplit('/', 1)[0]

#Exports selected objects as obj to projectFolder -> export folder. If you want a different file location, specify as exportPath
#specify single=True if you want all selected objects to be exported to separate files
def exportSelected(path='', single=False):
    selection = cmds.ls(selection=True, long=True)

    if '' == path:
        path = '{}/export'.format(cmds.workspace(query=True, rootDirectory=True).strip('/'))
        path = path.strip('/')

    if not os.path.exists(path):
        os.makedirs(path)

    if single:
        for s in selection:
            cmds.select(s, replace=True)
            filePath = '{}/{}.obj'.format(path, s.split('|')[-1])
            cmds.file(filePath, exportSelected=True, type='OBJexport', options='groups=0;ptgroups=0;materials=0;smoothing=1;normals=1')
    else:
        if len(selection) > 1:
            filePath = '{}/tempExport.obj'.format(path)
        else:
            filePath = '{}/{}.obj'.format(path, selection[0].split('|')[-1])

        cmds.file(filePath, exportSelected=True, type='OBJexport', options='groups=0;ptgroups=0;materials=0;smoothing=1;normals=1')
        sys.stdout.write("Exported to: {}".format(filePath))


def saveIncrementally():
    import re
    filename = cmds.file(sceneName=True, query=True)
    m = re.match('(.+)_v(\d{3})\.(.+)', filename)
    if 3 == len(m.groups()):
        filename = '{0}_v{1:03d}.{2}'.format(m.group(1), int(m.group(2)) + 1, m.group(3))
    cmds.file(rename=filename)
    cmds.file(save=True)
