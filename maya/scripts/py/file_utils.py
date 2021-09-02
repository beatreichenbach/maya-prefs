# A collections of file utility functions.
# **import_files**
# Import multiplie files and delete the mtl file when importing obj.
#
# Args:
#     remove_materials (boolean): Removes the .mtl files for .obj files. Default is True.
#
# **export_selected**
# Export selected to a specified temp directory as obj.
#
# Args:
#     path (string): Specify a path to export files to. Default is <project>/export
#     single (boolean): If set will export each selected object to a separate file. Default is false.
#
# **save_incremental**
# Save version up when using the v000 version pattern for naming.

from maya import cmds
import os
import sys
import re


last_imported_path = cmds.workspace(query=True, rootDirectory=True)


def import_files(remove_materials=True):
    global last_imported_path

    file_dialog = cmds.fileDialog2(
        caption='Import Files',
        startingDirectory=last_imported_path,
        fileMode=4,
        okCaption='Import')

    if not file_dialog:
        return
    for filepath in file_dialog:
        filepath = filepath.replace('\\', '/')
        filename, ext = os.path.splitext(os.path.basename(filepath))
        if 'mtl' == ext:
            continue

        if remove_materials:
            mtl_file = filepath.replace(ext, 'mtl')

            if os.path.isfile(mtl_file):
                os.remove(mtl_file)

        mesh = cmds.file(
            filepath,
            i=True,  # import the specified file
            ignoreVersion=True,
            renameAll=True,
            preserveReferences=True,
            returnNewNodes=True)

        if len(mesh) > 0:
            cmds.rename(mesh[0], filename)

    last_imported_path = os.path.dirname(filepath)


def export_selected(path='', single=False):
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
            cmds.file(
                filePath,
                exportSelected=True,
                type='OBJexport',
                options='groups=0;ptgroups=0;materials=0;smoothing=1;normals=1')
    else:
        if len(selection) > 1:
            filePath = '{}/tempExport.obj'.format(path)
        else:
            filePath = '{}/{}.obj'.format(path, selection[0].split('|')[-1])

        cmds.file(
            filePath,
            exportSelected=True,
            type='OBJexport',
            options='groups=0;ptgroups=0;materials=0;smoothing=1;normals=1')
        sys.stdout.write("Exported to: {}".format(filePath))


def save_incremental():
    filename = cmds.file(sceneName=True, query=True)
    m = re.match(r'(.+)_v(\d{3})\.(.+)', filename)
    if len(m.groups()) == 3:
        filename = '{0}_v{1:03d}.{2}'.format(m.group(1), int(m.group(2)) + 1, m.group(3))
    cmds.file(rename=filename)
    cmds.file(save=True)
