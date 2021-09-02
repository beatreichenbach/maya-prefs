import os
import shutil
import logging


def install():
    maya_app_dir = os.environ.get('MAYA_APP_DIR')
    if not maya_app_dir or not os.path.isdir(maya_app_dir):
        return

    current_directory = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(current_directory):
        if file.startswith('.'):
            continue

        if os.path.isfile(os.path.join(current_directory, file)):
            continue

        source = os.path.join(current_directory, file)
        target = os.path.join(maya_app_dir, file)

        shutil.copytree(source, target, dirs_exist_ok=True)


if __name__ == '__main__':
    install()
