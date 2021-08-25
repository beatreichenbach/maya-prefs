'''
  Author: Beat Reichenbach
  Date: 10/2/2015
  Version: 1.0

  Description: Import textures in Mudbox format into layer stack

  Code to run:
import br_renameObjects
br_renameObjects.renameObjectsUI()
'''

import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
import re
import shiboken
import maya.OpenMayaUI as apiUI

selection = []
def renameObjects():
    updateSelection()
    if not selection:
        return

    renameInputs = getInputs()
    oldName = resultElements[0].text()

    for s in selection:
        oldName = s.split('|')[-1]
        try:
            newName = re.sub(renameInputs[2], renameInputs[3], oldName)
        except re.error:
            newName = oldName
        newName = renameInputs[0] + re.sub(renameInputs[2], renameInputs[3], oldName) + renameInputs[1]
        cmds.rename(s,newName)
    updateSelection()

def updateResult():
    renameInputs = getInputs()
    oldName = resultElements[0].text()
    try:
        newName = re.sub(renameInputs[2], renameInputs[3], oldName)
    except re.error:
        newName = oldName

    newName = renameInputs[0] + newName + renameInputs[1]
    resultElements[1].setText(newName)

def updateSelection():
    global selection
    selection = cmds.ls(selection=True, shortNames=True)
    if selection:
        selectionStr = str(len(selection))
        selectionStr +=' Objects selected' if len(selection) > 1 else ' Object selected'
        selectedObjects.setText(selectionStr)
        resultElements[0].setText(selection[0].split('|')[-1])
        updateResult()

def getInputs():
    return (
        renameElements[1].text(),
        renameElements[3].text(),
        renameElements[5].text(),
        renameElements[7].text())

def renameObjectsUI():
    updateSelection()
    dialog.show()

#Get MayaWindow
ptr = apiUI.MQtUtil.mainWindow()
if ptr:
    mayaWindow = shiboken.wrapInstance(long(ptr), QtGui.QWidget)

#Creating Dialog
dialog = QtWidgets.QDialog(parent=mayaWindow)
dialog_layout = QtWidgets.QGridLayout()
dialog.setLayout(dialog_layout)

# Creating Layouts
rename_layout = QtWidgets.QGridLayout()
result_layout = QtWidgets.QGridLayout()
selection_layout = QtWidgets.QHBoxLayout()
resultNames_layout = QtWidgets.QHBoxLayout()
buttons_layout = QtWidgets.QHBoxLayout()

# Creating Widgets
rename_grp = QtWidgets.QGroupBox("Rename Options")
result_grp = QtWidgets.QGroupBox("Result")
renameLabels = ('Prefix', 'Suffix', 'Replace', 'With')
renameElements = []
for lbl in renameLabels:
    renameElements.append(QtWidgets.QLabel(text = lbl+':'))
    renameElements.append(QtWidgets.LineEdit())

selectedObjects = QtWidgets.QLabel()
updateSelection_btn = QtWidgets.QPushButton(text='Update Sel')

resultElements = []
for i in range(2):
    resultElements.append(QtWidgets.LineEdit())
    resultElements[i].setReadOnly(True)

ok_btn = QtWidgets.QPushButton(text='OK')
cancel_btn = QtWidgets.QPushButton(text='Cancel')

renameInputs = getInputs()

# Adding Widgets
for i, element in enumerate(renameElements):
    rename_layout.addWidget(element, i/4+1, i%4+1)
    if i%2:
        element.textEdited.connect(updateResult)

selection_layout.addWidget(selectedObjects)
selection_layout.addWidget(updateSelection_btn)

for i in range(2):
    resultNames_layout.addWidget(resultElements[i])

result_layout.addLayout(selection_layout,1,1)
result_layout.addLayout(resultNames_layout,2,1)

buttons_layout.addWidget(ok_btn)
buttons_layout.addWidget(cancel_btn)

rename_grp.setLayout(rename_layout)
result_grp.setLayout(result_layout)
dialog_layout.addWidget(rename_grp,1,1)
dialog_layout.addWidget(result_grp,2,1)
dialog_layout.addLayout(buttons_layout,3,1)

updateSelection_btn.clicked.connect(updateSelection)
ok_btn.clicked.connect(renameObjects)
cancel_btn.clicked.connect(dialog.reject)


class LineEdit(QtWidgets.QLineEdit):
    def keyPressEvent(self, event):
        if event.key() != QtCore.Qt.Key.Key_Control and event.key() != QtCore.Qt.Key.Key_Shift:
            super(LineEditSpaces, self).keyPressEvent(event)
