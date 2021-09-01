import sys
import os
import re

from PySide2 import QtCore, QtUiTools, QtWidgets
from shiboken2 import wrapInstance

from maya import cmds, OpenMayaUI
from .undo import undo


@undo
def renameNodes(**kwargs):
    # get objects
    selection = cmds.ls(selection=True, long=True)
    sortedSelection = sorted(selection, key=lambda longName: len(longName.split('|')), reverse=True)

    for node in sortedSelection:
        name = node.rsplit('|', 1)[-1]

        findReplace = kwargs.get('findReplace')
        if findReplace:
            find = findReplace.get('find', '')
            replace = findReplace.get('replace', '')

            flags = 0
            if not findReplace.get('caseSensitive'):
                flags &= re.IGNORECASE

            if not findReplace.get('regex'):
                find = re.escape(find)
                replace = replace

            if find:
                name = re.sub(find, replace, name, flags=flags)

        prefixSuffix = kwargs.get('prefixSuffix')
        if prefixSuffix:
            name = '{}{}{}'.format(
                prefixSuffix.get('prefix', ''),
                name,
                prefixSuffix.get('suffix', ''))

        numbering = kwargs.get('numbering')
        if numbering:
            index = selection.index(node)
            mode = numbering.get('mode')
            separator = numbering.get('separator', '')
            start = numbering.get('start', 1)
            increment = numbering.get('increment', 1)
            padding = numbering.get('padding', 0)

            number = '{number:{fill}{length}d}'.format(
                number=index * increment + start,
                fill=0,
                length=padding)

            if mode == 'Suffix':
                name = '{}{}{}'.format(name, separator, number)

        cmds.rename(node, name)
    return True


class RenameDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RenameDialog, self).__init__(parent)

        self._loadUI()
        self._connectUI()

    def _loadUI(self):
        loader = QtUiTools.QUiLoader()
        widget = loader.load(os.path.join(os.path.dirname(__file__), 'main.ui'))
        self.setLayout(widget.layout())
        self.__dict__.update(widget.__dict__)
        for element in self.__dict__.values():
            if isinstance(element, QtWidgets.QLineEdit):
                element.keyPressEvent = self._keyPressEvent

    def _connectUI(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def _keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key.Key_Control or key == QtCore.Qt.Key.Key_Shift:
            pass
        else:
            super(QtWidgets.QLineEdit, self).keyPressEvent(event)

    def accept(self):
        kwargs = {
            'findReplace': {
                'find': self.find_line.text(),
                'replace': self.replace_line.text(),
                'regex': self.regex_chk.checkState() == QtCore.Qt.Checked,
                'caseSensitive': self.case_chk.checkState() == QtCore.Qt.Checked
            },
            'prefixSuffix': {
                'prefix': self.prefix_line.text(),
                'suffix': self.suffix_line.text()
            },
            'numbering': {
                'mode': self.mode_cmb.currentText(),
                'start': self.start_spin.value(),
                'increment': self.increment_spin.value(),
                'padding': self.padding_spin.value(),
                'separator': self.separator_line.text()
            }
        }
        result = renameNodes(**kwargs)
        if not result:
            cmds.undo()


class LineEdit(QtWidgets.QLineEdit):
    # Bug when pressing shift in maya line edit widgets
    def keyPressEvent(self, event):
        if event.key() != QtCore.Qt.Key.Key_Control and event.key() != QtCore.Qt.Key.Key_Shift:
            super(LineEdit, self).keyPressEvent(event)


def show():
    OpenMayaUI.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)
    dialog = RenameDialog(mayaMainWindow)
    dialog.show()


def main():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    dialog = RenameDialog()
    dialog.show()
    app.exec_()


if __name__ == '__main__':
    main()
