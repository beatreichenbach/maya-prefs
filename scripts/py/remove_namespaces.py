# Deletes all namespaces
#
# Args:
#     name (string): Specify namespace to be removed.

from maya import cmds
import logging


def remove_namespaces(name=''):
    cmds.namespace(setNamespace=':')

    if name:
        namespaces = cmds.namespaceInfo(name, listOnlyNamespaces=True)
    else:
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)

    if not namespaces:
        return

    for namespace in ('UI', 'shared'):
        if namespace in namespaces:
            namespaces.remove(namespace)

    if not namespaces:
        return

    for namespace in namespaces:
        if cmds.namespaceInfo(namespace, listOnlyNamespaces=True):
            remove_namespaces(namespace)
        else:
            cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=namespace)
            logging.info('Namespace ' + namespace + 'removed.')

    remove_namespaces()
