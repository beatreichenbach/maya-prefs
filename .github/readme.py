import os
import shutil
import logging
import re


def create_readme():
    directories = ['scripts/hotkeys', 'scripts/py']
    current_directory = os.path.dirname(os.path.abspath(__file__))

    readme_path = '../README.md'

    with open(readme_path, 'w') as file:
        file.truncate(0)

    for directory in directories:
        path = os.path.join(current_directory, '..', directory)

        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            # handle package
            if os.path.isdir(item_path):
                file_path = os.path.join(item_path, '__init__.py')
                if not os.path.isfile(file_path):
                    continue

            # handle module
            elif os.path.isfile(item_path):
                file_path = item_path

            # read file and create text
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
                continue

            # add title
            filename, ext = os.path.splitext(item)
            item_text.insert(0, '### {}'.format(filename))
            # add empty line after
            item_text.append('')

            with open(readme_path, 'a') as file:
                file.write('\n'.join(item_text))


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    create_readme()
