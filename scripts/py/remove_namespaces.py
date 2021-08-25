'''
  Author: Beat Reichenbach
  Date: 7/11/2015
  Version: 1.0

  Description: Deletes all namespaces
  
  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_removeNamespaces
br_removeNamespaces.removeNamespaces()

'''

from maya import cmds

def removeNamespaces(name=''):
    cmds.namespace(setNamespace=':')
    namespaces = cmds.namespaceInfo(name, listOnlyNamespaces=True) if name else cmds.namespaceInfo(listOnlyNamespaces=True)
    if not namespaces:
        return
    for d in ('UI', 'shared'):
        if d in namespaces:
            namespaces.remove(d)
    if not namespaces:
        return
    for n in namespaces:
        if cmds.namespaceInfo(n, listOnlyNamespaces=True):
            removeNamespaces(n)
        else:
            cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=n)
            print 'Namespace ' + n + 'removed.'
    removeNamespaces()