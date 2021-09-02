import os
import shutil
import re


README = '''# maya-prefs
A maya setup with all my personal tools, hotkeys and shelves.


## Installation:

Move the contents of the maya folder into your maya [prefs location](https://knowledge.autodesk.com/support/maya/getting-started/caas/CloudHelp/cloudhelp/2022/ENU/Maya-Customizing/files/GUID-393D1ECA-9B6E-4625-B5B1-3F28E62AFB1C-htm.html).
This can be found here:

* **Windows:** <drive>:\Documents\maya
* **Mac OS X:** /Users/<username>/Library/Preferences/Autodesk/maya
* **Linux:** /home/<username>/maya

Alternatively you can set your own path with the environment variable `MAYA_APP_DIR`.
For my personal prefs I use the environment variable and use the install.py to copy the contents from the repository to the prefs folder.

'''


README_PATH = '../README.md'

def extract_docstring(script_path):
    '''Parses a file and extracts the first comment from it.
    Expects first line to start with a comment. Stops after first line that isn't commented.
    Only works with single line comments.

    Args:
        script_path (string): the path to the file or package

    Returns:
        (string): Rhe extracted comment.
    '''

    if os.path.isdir(script_path):
        file_path = os.path.join(script_path, '__init__.py')
        if not os.path.isfile(file_path):
            return
    elif os.path.isfile(script_path):
        file_path = script_path
    else:
        return

    item_text = []
    with open(file_path, 'r') as file:
        text = file.readlines()
        for line in text:
            match = re.search(r'^(?:#|//) ?(.*)', line)
            if match:
                item_text.append(match.group(1))
            else:
                break

    if not item_text:
        return

    # add title
    filename, ext = os.path.splitext(os.path.basename(script_path))
    item_text.insert(0, '### {}'.format(filename))

    # add new line at end
    item_text.append('')

    content = '\n'.join(item_text)

    return content


def add_section(header, dir_path):
    '''Adds a section to the readme file by parsing all files in given directory.

    Args:
        header (string): The section header.
        dir_path (string): The directory to list functions from.
    '''
    current_directory = os.path.dirname(os.path.abspath(__file__))

    path = os.path.join(current_directory, '..', dir_path)

    content = []

    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        # read file and create text
        docstring = extract_docstring(file_path)

        if docstring:
            content.append(docstring)

    if content:
        with open(README_PATH, 'a') as file:
            file.write('## {}\n'.format(header))
            file.write('\n'.join(content))


def create_readme():
    with open(README_PATH, 'w') as file:
        file.truncate(0)
        file.write(README)

    add_section('Hotkeys', 'maya/scripts/hotkeys')
    add_section('Scripts', 'maya/scripts/py')


if __name__ == '__main__':
    create_readme()
