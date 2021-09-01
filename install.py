import os
import shutil
import logging


def install():
    maya_app_dir = os.environ.get('MAYA_APP_DIR')
    if not maya_app_dir or not os.path.isdir(maya_app_dir):
        return

    directories = [
        '2022',
        'scripts']

    current_directory = os.path.dirname(os.path.abspath(__file__))

    for directory in directories:
        source = os.path.join(current_directory, directory)
        target = os.path.join(maya_app_dir, directory)

        shutil.copytree(source, target, dirs_exist_ok=True)


if __name__ == '__main__':
    install()
