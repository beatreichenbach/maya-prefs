# Extract the currently selected faces from the object without separating different shells. Slow!

import pymel.core as pm


def extract_faces():
    faces = pm.ls(sl=True)
    facesNum = []
    for f in faces:
        facesNum.extend(f.indices())

    origTransform = pm.listRelatives(pm.listRelatives(p=True)[0], p=True)[0]
    newTransform = pm.duplicate(origTransform)[0]

    pm.delete(origTransform.f[facesNum])
    pm.select(newTransform.f[:], r=True)
    pm.select(newTransform.f[facesNum], d=True)
    pm.delete()
