'''
  Author: Beat Reichenbach
  Date: 07/08/2017
  Version: 1.0

  Description: Import multiplie files and delete the mtl file when importing obj. Export selected to a specified temp directory as obj.
  
  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_assignShader
br_assignShader.ui()

'''

from maya import cmds

class AssignShader:
    def __init__(self):
        self.window = 'assignShaderWindow'
        self.mainForm = ''
        
        self.shaderLayout = ''
        
        self.shaders = []
        
    def deleteWindow(self, *args):
        cmds.deleteUI(self.window)  
        
    def show(self):
        if cmds.window(self.window, exists=True):
            self.deleteWindow()
        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)
        
        cmds.window(self.window, title='Assign Shader', widthHeight=(220, 60), sizeable=False)
        
        self.mainForm = cmds.columnLayout()
        funcForm = cmds.formLayout()

        generateButton = cmds.button(label='Add', width=80, command=self.add)
        clearButton = cmds.button(label='Clear', width=80, command=self.clear)
        
        cmds.formLayout(funcForm, edit=True, attachForm=[(generateButton, 'left', 20), (generateButton, 'top', 20)])
        cmds.formLayout(funcForm, edit=True, attachForm=[(clearButton, 'left', 120), (clearButton, 'top', 20)])
        
        cmds.setParent(self.mainForm)
        self.shaderLayout = cmds.formLayout()
        
        cmds.showWindow(self.window)
    
    def add(self, *args):
        self.shaders.extend([shader for shader in cmds.ls(selection=True, mat=True) if shader not in self.shaders])
        
        cmds.deleteUI(self.shaderLayout)
        cmds.setParent(self.mainForm)
        self.shaderLayout = cmds.formLayout()
        
        #shaderButtons = [cmds.button(label=shader, width=180, command=self.assignShader) for shader in self.shaders]
        shaderButtons = []
        for shader in self.shaders:
            if cmds.objectType(shader, isType='VRayMtl'):
                color = cmds.getAttr(shader + '.color')[0]
                color = [pow(c, .4545) for c in color]
                shaderButtons.append(cmds.button(label=shader, width=180, command='br_assignShader.assignShader("{}")'.format(shader), backgroundColor=color))
                print 'br_assignShader.assignShader({})'.format(shader)
            else:
                shaderButtons.append(cmds.button(label=shader, width=180, command='br_assignShader.assignShader("{}")'.format(shader)))
        
        for i, button in enumerate(shaderButtons):
            cmds.formLayout(self.shaderLayout, edit=True, attachForm=[(button, 'left', 20), (button, 'top', i*40 + 20)])
        cmds.window(self.window, edit=True, widthHeight=(220, (len(shaderButtons)*40 + 60)))
    
    def clear(self, *args):
        cmds.window(self.window, edit=True, widthHeight=(220, 60))
        cmds.deleteUI(self.shaderLayout)
        self.shaders = []
        cmds.setParent(self.mainForm)
        self.shaderLayout = cmds.formLayout()
    
    def assignShader(self, shader, *args):
        cmds.sets(cmds.ls(selection=True, long=True), edit=True, forceElement=cmds.listConnections(shader + '.outColor', d=True)[0])
#

assignShaderTool = AssignShader()
        
def assignShader(shader):
    cmds.sets(cmds.ls(selection=True, long=True), edit=True, forceElement=cmds.listConnections(shader + '.outColor', d=True)[0])
    
def ui():
    assignShaderTool.show()
    
