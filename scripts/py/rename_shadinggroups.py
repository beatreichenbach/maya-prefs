# Rename ShadingGroup nodes to match their incoming material.

from maya import cmds


def rename_shadinggroups():
    shadinggroups = cmds.ls(selection=True, type='shadingEngine')
    if not shadinggroups:
        shadinggroups = cmds.ls(type='shadingEngine')

    for shadinggroup in shadinggroups:
        shader = cmds.listConnections('{}.surfaceShader'.format(shadinggroup), source=True)[0]
        for ext in ['_mtl', '_shd']:
            if ext in shader:
                cmds.rename(shadinggroup, shader.replace(ext, '_sg'))
                break
