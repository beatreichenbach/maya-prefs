'''
  Author: Beat Reichenbach
  Date: 10/09/2015
  Version: 1.1

  Description: Different small functions for production

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.

import br_createCamera
br_createCamera.createCamera()


'''

from maya import cmds

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
