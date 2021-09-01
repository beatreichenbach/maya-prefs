# Creates a camera from the current view in the active panel.

from maya import cmds


def create_camera(name='shotCam'):
    sourceCam = cmds.modelPanel(cmds.getPanel(withFocus=True), query=True, camera=True)
    cam = cmds.camera()[0]
    cam = cmds.rename(cam, name)
    ratio = cmds.getAttr('defaultResolution.deviceAspectRatio')
    cam_shape = cmds.listRelatives(cam, shapes=True)[0]
    cmds.setAttr('{}.focalLength'.format(cam_shape), 50)
    cmds.setAttr('{}.horizontalFilmAperture'.format(cam_shape), ratio)
    cmds.setAttr('{}.locatorScale'.format(cam_shape), 10)

    translation = cmds.xform(sourceCam, worldSpace=True, translation=True, query=True)
    rotation = cmds.xform(sourceCam, worldSpace=True, rotation=True, query=True)
    cmds.xform(cam, worldSpace=True, translation=translation, rotation=rotation)
