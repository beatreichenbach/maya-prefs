'''
  Author: Beat Reichenbach
  Date: 8/17/2015
  Version: 1.0

  Description: Selects faces by normal (define threshold angle as parameter)

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_selectByNormal
br_selectByNormal.selectByNormal(60)

'''

from maya import cmds
import re


def selectByNormal(angle=60):
    selection = cmds.ls(selection=True)
    if not selection:
        return
    object = selection[0].split('.')[0]
    
    selectedFaces = []
    for s in cmds.ls(selection=True):
        groups = re.search('f\[(\d+):?(\d+)?\]', s)
        if not groups:
            continue
        if len(groups.groups()) == 3:
            selectedFaces.append(range(int(groups.group(1)), int(groups.group(2))))
        else:
            selectedFaces.append(groups.group(1))
    
    vectors = []
    for f in selectedFaces:
        faceNormal = cmds.polyInfo('{}.f[{}]'.format(object, f), faceNormals=True)[0]
        vectors.append([float(faceNormal.rsplit(' ', 3)[j]) for j in range(-3, 0)]) 
   
    faces = []
    normals = cmds.polyInfo(object, faceNormals=True)
    for i in range(cmds.polyEvaluate(object, f=True)):
        normal = [float(normals[i].rsplit(' ', 3)[j]) for j in range(-3, 0)]
        for vector in vectors:
            dotProduct = sum(p*q for p,q in zip(normal, vector))
            if dotProduct + angle/180.0 > 1:
                faces.append(i)

    cmds.select(clear=True)
    for f in faces:
        cmds.select('{}.f[{}]'.format(object, f), add=True)