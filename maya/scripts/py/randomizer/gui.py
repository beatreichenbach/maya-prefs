import sys
import os
import random

from PySide2 import QtUiTools, QtWidgets

from maya import cmds

ATTRNAMES = {
    'translation': 'translate',
    'rotation': 'rotate',
    'scale': 'scale'}


def get_selection():
    objects = {}
    for i, obj in enumerate(cmds.ls(selection=True, long=True)):
        data = {}
        data['translation'] = cmds.getAttr('{}.translate'.format(obj))[0]
        data['rotation'] = cmds.getAttr('{}.rotate'.format(obj))[0]
        data['scale'] = cmds.getAttr('{}.scale'.format(obj))[0]
        data['selected'] = True
        data['seed'] = i
        objects[obj] = data
    return objects


def select_random(objects, kwargs):
    cmds.select(clear=True)
    if kwargs['type'] == 'percentage':
        for i, obj in enumerate(objects.keys()):
            random.seed(i)
            if random.random() > (100 - kwargs['value']) / 100:
                cmds.select(obj, add=True)


def apply_transforms(objects, kwargs):
    for obj, data in objects.items():
        for i, attribute in enumerate(('translation', 'rotation', 'scale')):
            xform = []
            for j, (t, d) in enumerate(zip(data[attribute], kwargs[attribute])):
                random.seed(data['seed'] + 0.5 * (i + j) * (i + j + 1) + j)

                if type(d) == float:
                    transform = t + d * (random.random() - 0.5) * 2
                elif type(d) == list and range(int(d[0]), int(d[1])):
                    transform = t + random.randrange(d[0], d[1])
                else:
                    transform = t

                if kwargs['space'] == 'Absolute':
                    transform -= t
                    if attribute == 'scale':
                        transform += 1
                xform.append(transform)

            if attribute == 'scale' and kwargs['uniform']:
                xform = [xform[0]] * 3
            cmds.setAttr('{}.{}'.format(obj, ATTRNAMES.get(attribute)), *xform)


class RandomizeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RandomizeDialog, self).__init__(parent)

        self._load_ui()
        self._connect_ui()

        cmds.undoInfo(openChunk=True)

        try:
            self.objects = get_selection()
        except ValueError:
            return

    def _load_ui(self):
        loader = QtUiTools.QUiLoader()
        widget = loader.load(os.path.join(os.path.dirname(__file__), 'main.ui'))
        self.setWindowTitle(widget.windowTitle())
        self.setLayout(widget.layout())
        self.__dict__.update(widget.__dict__)

    def _connect_ui(self):
        # randomize
        self.randomize_uniform_chk.toggled.connect(self.randomize_scale_y_spn.setDisabled)
        self.randomize_uniform_chk.toggled.connect(self.randomize_scale_z_spn.setDisabled)
        self.randomize_uniform_chk.toggled.connect(self.update)

        for attribute in ('translation', 'rotation', 'scale'):
            for component in ('x', 'y', 'z'):
                spinner = getattr(self, 'randomize_{}_{}_spn'.format(attribute, component))
                spinner.valueChanged.connect(self.update)

        self.randomize_space_cmb.currentIndexChanged.connect(self.update)

        # random range
        self.randomrange_uniform_chk.toggled.connect(self.randomrange_scale_miny_spn.setDisabled)
        self.randomrange_uniform_chk.toggled.connect(self.randomrange_scale_maxy_spn.setDisabled)
        self.randomrange_uniform_chk.toggled.connect(self.randomrange_scale_minz_spn.setDisabled)
        self.randomrange_uniform_chk.toggled.connect(self.randomrange_scale_maxz_spn.setDisabled)
        self.randomrange_uniform_chk.toggled.connect(self.update)

        for attribute in ('translation', 'rotation', 'scale'):
            for component in ('x', 'y', 'z'):
                for t in ('min', 'max'):
                    spinner = getattr(self, 'randomrange_{}_{}{}_spn'.format(attribute, t, component))
                    spinner.valueChanged.connect(self.update)

        self.randomrange_space_cmb.currentIndexChanged.connect(self.update)

        # select random
        self.select_percentage_spn.valueChanged.connect(self.update)

        # dialog
        self.main_btnbox.accepted.connect(self.accept)
        self.main_btnbox.rejected.connect(self.reject)

    def update(self):
        tab_widget = self.layout().itemAt(0).widget()
        tab = tab_widget.tabText(tab_widget.currentIndex())

        if tab == 'Randomize':
            kwargs = {}
            for attribute in ('translation', 'rotation', 'scale'):
                values = []
                for component in ('x', 'y', 'z'):
                    spinner = getattr(self, 'randomize_{}_{}_spn'.format(attribute, component))
                    values.append(spinner.value())
                kwargs[attribute] = values
            kwargs['uniform'] = self.randomize_uniform_chk.isChecked()
            kwargs['space'] = self.randomize_space_cmb.currentText()
            apply_transforms(self.objects, kwargs)

        if tab == 'Random Range':
            kwargs = {}
            for attribute in ('translation', 'rotation', 'scale'):
                values = []
                for component in ('x', 'y', 'z'):
                    trange = []
                    for a in ('min', 'max'):
                        spinner = getattr(self, 'randomrange_{}_{}{}_spn'.format(attribute, a, component))
                        trange.append(spinner.value())
                    values.append(trange)
                kwargs[attribute] = values
            kwargs['uniform'] = self.randomrange_uniform_chk.isChecked()
            kwargs['space'] = self.randomrange_space_cmb.currentText()
            apply_transforms(self.objects, kwargs)

        if tab == 'Select Random':
            kwargs = {}
            kwargs['type'] = 'percentage'
            kwargs['value'] = self.select_percentage_spn.value()
            select_random(self.objects, kwargs)

    def accept(self):
        cmds.select(list(self.objects.keys()), replace=True)
        cmds.undoInfo(closeChunk=True)

        super(RandomizeDialog, self).accept()

    def reject(self):
        cmds.select(list(self.objects.keys()), replace=True)

        for obj, data in self.objects.items():
            for attribute in ('translation', 'rotation', 'scale'):
                cmds.setAttr('{}.{}'.format(obj, ATTRNAMES.get(attribute)), *data[attribute])
        cmds.undoInfo(closeChunk=True)

        super(RandomizeDialog, self).reject()


def show():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    main_window = next(w for w in app.topLevelWidgets() if w.objectName() == 'MayaWindow')
    dialog = RandomizeDialog(main_window)
    dialog.show()
    return main_window


def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    dialog = RandomizeDialog()
    dialog.show()
    app.exec_()


if __name__ == '__main__':
    main()
