import os
import sys
import subprocess
import logging

from maya import cmds


def set_env():
    # setting env vars
    maya_app_dir = os.environ['MAYA_APP_DIR'] or cmds.internalVar(userPrefDir=True)
    maya_app_dir = os.path.abspath(maya_app_dir)
    maya_script_dir = os.path.join(maya_app_dir, 'scripts')

    os.environ['MAYA_SCRIPT_PATH'] += os.pathsep + os.path.join(maya_script_dir, '_mel')
    os.environ['MAYA_SCRIPT_PATH'] += os.pathsep + os.path.join(maya_script_dir, '_hotkeys')
    os.environ['MAYA_PLUG_IN_PATH'] += os.pathsep + os.path.join(maya_app_dir, 'plugins')
    sys.path.append(os.path.join(maya_script_dir, '_py'))
    sys.path.append(r'D:/files/dev/021_textureimporter')


def load_yeti():
    os.environ['peregrinel_LICENSE'] = r'C:\Program Files\Yeti\yeti.lic'
    subprocess.Popen(r'C:\Program Files\Yeti\rlm\rlm.exe', shell=True)


def startup():
    cmds.hotkeySet('Custom', edit=True, current=True)
    from reorderAttributes.ui import install
    install()


set_env()
# load_yeti()
if not cmds.about(batch=True):
    cmds.evalDeferred(startup)

logging.info('Loaded userSetup.py successfully')
