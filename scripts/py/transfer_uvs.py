'''
  Author: Beat Reichenbach
  Date: 9/1/2015
  Version: 1.0

  Description: Transfer UVs to multiple objects

  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_transferUVs
br_transferUVs.ui()

'''

from maya import cmds

window = 'transferUVsWindow'

def transferUVs():
    sampleSpace = cmds.radioButtonGrp('sampleSpace_radio', query=True, select=True)
    sampleSpace = (0,1,4,5)[sampleSpace - 1]

    method = cmds.radioButtonGrp('method_radio', query=True, select=True)
    method = (0,3)[method - 1]
    
    deleteHistory = True if cmds.radioButtonGrp('deleteHistory_radio', query=True, select=True) == 2 else False
    
    objects = cmds.ls(sl=True,type='transform')
    source = cmds.ls(sl=True,head=True)
    objects.remove(source[0])
    for o in objects:
        cmds.transferAttributes(source, o, uvs=1, sampleSpace=sampleSpace, searchMethod=method)
        if deleteHistory:
            cmds.delete(o, ch=True)
        
def deleteWindow():
    cmds.deleteUI(window)
        
def ui():
    if cmds.window(window, exists=True):
        deleteWindow()
    if cmds.windowPref(window, exists=True):
        cmds.windowPref(window, remove=True)
    
    cmds.window(window, title='Transfer UVs', widthHeight=(550, 150), sizeable=False)
    form = cmds.formLayout()
    frame = cmds.frameLayout(borderVisible=True, labelVisible=False, width=530, height=100)
    cmds.formLayout(form, edit=True, attachForm=[(frame, 'left', 10), (frame, 'top', 10)])
    
    settings_form = cmds.formLayout()
    sampleSpace_radio = cmds.radioButtonGrp('sampleSpace_radio', label='Sample Space:', labelArray4=['World', 'Local', 'Component', 'Topology'], numberOfRadioButtons=4)
    cmds.radioButtonGrp(sampleSpace_radio, edit=True, select=4)
    
    method_radio = cmds.radioButtonGrp('method_radio', label='Search Method:', labelArray2=['Closest along norm.', 'Closest to point'], numberOfRadioButtons=2)
    cmds.radioButtonGrp(method_radio, edit=True, select=2)
    
    deleteHistory_radio = cmds.radioButtonGrp('deleteHistory_radio', label='History:', labelArray2=['Keep', 'Delete'], numberOfRadioButtons=2)
    cmds.radioButtonGrp(deleteHistory_radio, edit=True, select=2)
    
    cmds.formLayout(settings_form, edit=True, attachForm=[(sampleSpace_radio, 'left', -50), (sampleSpace_radio, 'top', 10)])
    cmds.formLayout(settings_form, edit=True, attachForm=[(method_radio, 'left', -50), (method_radio, 'top', 40)])
    cmds.formLayout(settings_form, edit=True, attachForm=[(deleteHistory_radio, 'left', -50), (deleteHistory_radio, 'top', 70)])
    
    cmds.setParent(form)
    buttons = []
    buttons.append(cmds.button(label='Transfer', width=170, command='br_transferUVs.transferUVs();br_transferUVs.deleteWindow()'))
    buttons.append(cmds.button(label='Apply', width=170, command='br_transferUVs.transferUVs()'))
    buttons.append(cmds.button(label='Close', width=170, command='br_transferUVs.deleteWindow()'))
    cmds.formLayout(form, edit=True, attachForm=[(buttons[0], 'left', 10), (buttons[0], 'top', 120)])
    cmds.formLayout(form, edit=True, attachForm=[(buttons[1], 'left', 190), (buttons[1], 'top', 120)])
    cmds.formLayout(form, edit=True, attachForm=[(buttons[2], 'left', 370), (buttons[2], 'top', 120)])
    cmds.showWindow(window)
