import os
import sys
import logging
from maya import cmds


def startup():
    logging.info('Loading userSetup.py...')

    maya_app_dir = os.environ['MAYA_APP_DIR'] or cmds.internalVar(userPrefDir=True)
    maya_app_dir = os.path.abspath(maya_app_dir)
    maya_script_dir = os.path.join(maya_app_dir, 'scripts')

    os.environ['MAYA_PLUG_IN_PATH'] += os.pathsep + os.path.join(maya_app_dir, 'plugins')
    os.environ['MAYA_SCRIPT_PATH'] += os.pathsep + os.path.join(maya_script_dir, 'external')
    os.environ['MAYA_SCRIPT_PATH'] += os.pathsep + os.path.join(maya_script_dir, 'hotkeys')
    sys.path.append(os.path.join(maya_script_dir, 'py'))
    sys.path.append(os.path.join(maya_script_dir, 'external'))

    if not cmds.about(batch=True):
        cmds.hotkeySet('Custom', edit=True, current=True)


cmds.evalDeferred(startup, lowestPriority=True)
