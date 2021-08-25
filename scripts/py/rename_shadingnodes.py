from maya import cmds

renameNodes():
    for s in cmds.ls(selection=True, type='shadingEngine'):
        cmds.rename(s, cmds.listConnections(s+'.outColor')[0].replace('shd', 'sg'))
    
    for s in cmds.ls(selection=True, type='file'):
        cmds.rename(s, cmds.listConnections(s+'.outColor')[0].replace('shd', 'sg'))