'''
  Author: Beat Reichenbach
  Date: 02/14/2017
  Version: 1.1

  Description: Curve tools to instance and place along curve.
  
  Installation: 1. Copy the script to your maya profile, %USERPROFILE%\Documents\maya\scripts
                2. Script is now available as a python module
                3. Put the code below in a button (make sure to set it to python) or run in a python script window.
  
import br_curveTools
br_curveTools.ui()

'''

from maya import cmds
import random as rand
from maya import mel
from functools import partial



class CurveTools:
    def __init__(self):
        self.window = 'curveToolsWindow'
        self.deformer = ''
        self.locator = ''
        self.baseWireCurve = ''
        self.deformCurve = ''
        self.previewGeo = ''
        self.curveInfo = ''
        
        
    def deleteWindow(self, *args):
        cmds.deleteUI(self.window)  
        
    def show(self):
        if cmds.window(self.window, exists=True):
            self.deleteWindow()
        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)
        
        cmds.window(self.window, title='Curve Tools', widthHeight=(200, 100), sizeable=False)
        
        form = cmds.formLayout()
        
        self.buttons = []
        self.buttons.append(cmds.button(width=120, command=self.deformerToggle))
        self.buttons.append(cmds.iconTextButton(style='iconOnly', label='Deformer', width=24, height=24))
        
        self.buttons.append(cmds.button(label='Preview', width=75, command=self.preview))
        self.buttons.append(cmds.button(label='Finalize', width=75, command=self.finalize))
        
        self.buttons.append(cmds.button(label='Toggle Deformer', width=160, command=self.toggleDeformer))
        
        self.buttons.append(cmds.button(label='Add', width=75, command=self.addGeometry))
        self.buttons.append(cmds.button(label='Remove', width=75, command=self.removeGeometry))
        
        self.buttons.append(cmds.button(label='Match Base', width=75, command=self.matchBase))
        self.buttons.append(cmds.button(label='Reset Base', width=75, command=self.resetBase))
        
        self.buttons.append(cmds.button(label='Rebuild Curves', width=160, command=self.rebuildCurve))
        
        self.buttons.append(cmds.button(label='Fillet', width=75, command=self.fillet))
        self.buttons.append(cmds.button(label='Complete', width=75, command=self.filletComplete))
        
        self.buttons.append(cmds.button(label='Close', width=160, command=self.deleteWindow))
        
        cmds.window(self.window, edit=True, widthHeight=(200, ((len(self.buttons) - 5) * 40 + 20)))
        
        
        offsets = [[0, 0], [136, 0], [0, 1], [85, 1], [0, 2], [0, 3], [85, 3], [0, 4], [85, 4], [0, 5], [0, 6], [85, 6], [0, 7]]
        for i, button in enumerate(self.buttons):
            cmds.formLayout(form, edit=True, attachForm=[(button, 'left', offsets[i][0] + 20), (button, 'top', offsets[i][1] * 40 + 20)])
        
        self.deformerToggleUpdate()
        
        cmds.showWindow(self.window)
        
    def deformerExists(self):
        return cmds.objExists(self.deformer)
       
    def deformerToggleUpdate(self):
        deformerExists = self.deformerExists()
        cmds.button(self.buttons[0], edit=True, label=('Clear Deformer' if deformerExists else 'Set Deformer'))
        cmds.iconTextButton(self.buttons[1], edit=True, image1=('precompExportChecked.png' if deformerExists else 'precompExportUnchecked.png'))

    def deformerToggle(self, *args):
        if self.deformerExists():
            self.deformer = ''
            self.deformerToggleUpdate()
        else:
            for s in cmds.ls(selection=True):
                for node in mel.eval('findRelatedDeformer("{}")'.format(s)):
                    if cmds.nodeType(node) == 'wire':
                        self.deformer = node
                        self.deformCurve = cmds.listConnections(self.deformer + '.deformedWire[0]', destination=True)[0]
                        self.baseWireCurve = cmds.listConnections(self.deformer + '.baseWire[0]', destination=True)[0]
                        self.deformerToggleUpdate()
                        return
            self.deformer = ''
            self.deformerToggleUpdate()

    def createPreviewGeo(self):
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning('Nothing selected!')
            return False
        self.curve = selection[0]        
        
        geoNodes = cmds.polyCylinder(sx=8, sy=1, sz=0, radius=1, height=1, axis=[1,0,0], name='reference')
        referenceGeo = geoNodes[0]
        creator = geoNodes[1]
        
        cmds.move(-0.5, 0, 0, [referenceGeo + '.scalePivot', referenceGeo + '.rotatePivot'], absolute=True)
        cmds.move(0.5, 0, 0, referenceGeo, relative=True)
        cmds.makeIdentity(referenceGeo, apply=True, t=True)
        
        self.previewGeo = cmds.duplicate(referenceGeo, ic=True, name='preview')[0]
        
        locatorNodes = cmds.circle(normal=[1,0,0], sections=8, name='deformerHandle')
        self.locator = locatorNodes[0]
        cmds.scale(1, 2.5, 2.5)
        
        cmds.addAttr(longName='subdivisions', niceName='Subdivisions', attributeType='long', min=0, defaultValue=64)
        cmds.addAttr(longName='radius', niceName='Radius', attributeType='float', min=0, defaultValue=4)
        cmds.connectAttr(self.locator + '.subdivisions', creator + '.subdivisionsHeight')
        cmds.connectAttr(self.locator + '.radius', creator + '.radius')
        cmds.connectAttr(self.locator + '.radius', locatorNodes[1] + '.radius')
        cmds.setAttr(self.locator + '.subdivisions', keyable=True)
        cmds.setAttr(self.locator + '.radius', keyable=True)
        for axis in ('x', 'y', 'z'):
            cmds.setAttr(self.locator + '.s' + axis, keyable=False)
        
        for s in [referenceGeo, self.previewGeo]:
            cmds.setAttr(s + '.overrideEnabled', 1)
            cmds.setAttr(s + '.overrideShading', 0)
            cmds.setAttr(s + '.overrideDisplayType', 2)
        
        cmds.parent(referenceGeo, self.locator)
        cmds.parent(self.previewGeo, self.locator)

        cmds.setAttr(self.locator + '.sx', cmds.arclen(self.curve))
        
    def createWire(self):
        self.deformCurve = cmds.curve(degree=1, p=[(0, 0, 0), (cmds.arclen(self.curve), 0, 0)], k=[0, 1], name='deformCurve')
    
        wireNodes = cmds.wire(self.previewGeo, wire=self.deformCurve)
        self.deformer = wireNodes[0]
        cmds.setAttr(self.deformer + '.dropoffDistance[0]', 10000)
        self.deformerToggleUpdate()
        
        self.baseWireCurve = cmds.listConnections(self.deformer + '.baseWire[0]', destination=True)[0]
        
        cmds.select(self.deformCurve, replace=True)
        cmds.select(self.curve, add=True)
        
        self.matchCurves()
        
        cmds.delete(self.curve)

    def preview(self, *args):
        if self.deformerExists():
            cmds.select(self.deformCurve)
            self.createPreviewGeo()
            cmds.delete(cmds.parentConstraint(self.baseWireCurve, self.locator))
            cmds.select(self.previewGeo)
            self.addGeometry()
        else:
            self.createPreviewGeo()
            self.createWire()
        
        self.curveInfo = cmds.arclen(self.deformCurve, ch=True)
        cmds.connectAttr(self.curveInfo + '.arcLength', self.locator + '.scaleX')
        
        cmds.parent(self.baseWireCurve, self.locator)
        cmds.select(self.locator)
        
    
    def finalize(self, *args):
        if not self.deformerExists():
            return
        if not self.locator:
            self.locator = cmds.listRelatives(self.baseWireCurve, parent=True, type='transform')[0]
        if not self.curveInfo:
            self.curveInfo = cmds.listConnections(cmds.listRelatives(self.deformCurve, shapes=True, pa=True), type='curveInfo')[0]
        cmds.parent(self.baseWireCurve, world=True)
        cmds.delete([self.locator, self.curveInfo])
        
    def matchCurves(self, *args):
        if len(cmds.ls(selection=True)) < 2:
            return
        source = cmds.ls(selection=True)[0]
        target = cmds.ls(selection=True)[1]
        
        cmds.rebuildCurve(source, ch=False, spans=cmds.getAttr(target + '.spans'), degree=cmds.getAttr(target + '.degree'))
        
        cv = 0
        while True:
            targetCv = '{}.cv[{}]'.format(target, cv)
            cmds.select(targetCv, replace=True)
            if cmds.ls(selection=True)[0] != targetCv:
                break
            cmds.xform('{}.cv[{}]'.format(source, cv), worldSpace=True, translation=cmds.pointPosition(targetCv, world=True))
            cv += 1
     
    def matchBase(self, *args):
        if not self.deformerExists():
            return
        
        source = cmds.duplicate(self.deformCurve, name='curvePiece')[0]
        numSpans = cmds.getAttr(source + '.spans')
        
        cmds.reverseCurve(source, replaceOriginal=True, ch=False)
        
        cmds.rebuildCurve(self.baseWireCurve, ch=False, spans=numSpans)
        curvePiece = source
        for i in range(numSpans - 1):
            previous = curvePiece
            curvePiece = cmds.detachCurve(curvePiece + '.ep[1]', ch=False, replaceOriginal=True, name='curvePiece')[0]
            cmds.delete(previous)
            cmds.move(cmds.arclen(curvePiece, ch=False), 0, 0, '{}.ep[{}]'.format(self.baseWireCurve, numSpans - i - 1), objectSpace=True, worldSpaceDistance=True)
        cmds.delete(curvePiece)
    
    def resetBase(self, *args):
        if not self.deformerExists():
            return
            
        source = self.deformCurve
        target = self.baseWireCurve
        cmds.rebuildCurve(target, ch=False, spans=cmds.getAttr(source + '.spans'), degree=cmds.getAttr(source + '.degree'))
     
    def toggleDeformer(self, *args):
        if not self.deformerExists():
            return
        cmds.setAttr(self.deformer + '.envelope', not cmds.getAttr(self.deformer + '.envelope'))
    
    def addGeometry(self, *args):
        if not self.deformerExists():
            return
        cmds.wire(self.deformer, edit=True, geometry=cmds.ls(selection=True))
        
    def removeGeometry(self, *args):
        if not self.deformerExists():
            return
        selection = cmds.ls(selection=True)
        cmds.wire(self.deformer, edit=True, geometry=selection, remove=True)
        cmds.delete(selection, ch=True)
        self.deformerToggleUpdate()
        
    def rebuildCurve(self, *args):
        mel.eval('RebuildCurveOptions')
        
    def fillet(self, *args):
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning('Nothing selected!')
            return false
        
        self.source = cmds.ls(selection=True)[0]

        cv = 0
        self.curves = []
        while True:
            cvA = '{}.cv[{}]'.format(self.source, cv)
            cvB = '{}.cv[{}]'.format(self.source, cv+1)
            cmds.select(cvB, replace=True)
            if cmds.ls(selection=True)[0] != cvB:
                break
            self.curves.append(cmds.curve(degree=1, p=[cmds.pointPosition(cvA, world=True), cmds.pointPosition(cvB, world=True)], k=[0, 1], name='curvePart'))
            cv += 1

        cmds.select(self.source, r=True)
        cmds.addAttr(longName='radius', niceName='Radius', attributeType='float', min=0, defaultValue=1)
        cmds.setAttr(self.source + '.radius', keyable=True)
            
        self.fillets = []
        for i in range(1, len(self.curves)):
            fillet = cmds.filletCurve(self.curves[i-1], self.curves[i], cp1=0, cp2=0, ch=True, name='curveFillet')
            self.fillets.append(fillet[0])
            cmds.connectAttr(self.source + '.radius', fillet[1] + '.radius')
        
        cmds.select(self.source)

        self.lastCV = cvA


    def createCurvePiece(self, cvA, cvB):
        return cmds.curve(degree=1, p=[cmds.pointPosition(cvA, world=True), cmds.pointPosition(cvB, world=True)], k=[0, 1], name='curvePiece')
         
        
    def filletComplete(self, *args):
        cmds.deleteAttr(self.source + '.radius')
        
        cmds.delete(self.curves)

        curvePieces = []
        curvePieces.append(self.createCurvePiece(self.source + '.cv[0]', self.fillets[0] + '.cv[0]'))
        for i in range(1, len(self.curves) - 1):
            curvePieces.append(self.createCurvePiece(self.fillets[i-1] + '.cv[3]', self.fillets[i] + '.cv[0]'))
        curvePieces.append(self.createCurvePiece(self.fillets[i] + '.cv[3]', self.lastCV))
        
        allPieces = curvePieces + self.fillets
        result = cmds.attachCurve(allPieces, ch=False, kmk=True)[0]

        allPieces.remove(result)
        cmds.delete(allPieces)
        cmds.select(result)
        cmds.rename(result, 'filletCurve')

#

curveTools = CurveTools()
        
def ui():
    curveTools.show()