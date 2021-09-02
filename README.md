# maya-prefs
A maya setup with all my personal tools, hotkeys and shelves.


## Installation:

Move the contents of the maya folder into your maya [prefs location](https://knowledge.autodesk.com/support/maya/getting-started/caas/CloudHelp/cloudhelp/2022/ENU/Maya-Customizing/files/GUID-393D1ECA-9B6E-4625-B5B1-3F28E62AFB1C-htm.html).
This can be found here:

**Windows:** <drive>:\Documents\maya
**Mac OS X:** /Users/<username>/Library/Preferences/Autodesk/maya
**Linux:** /home/<username>/maya

Alternatively you can set your own path with the environment variable `MAYA_APP_DIR`.
For my personal prefs I use the environment variable and use the install.py to copy the contents from the repository to the prefs folder.

## Scripts:

### Hotkeys
#### changeGridDivisions
Halves or doubles the divisions on the viewport grid.

Args:
    smaller (boolean): Havles the number of divisions.
    bigger (boolean): Doubles the number of divisions.
### Hotkeys
#### pasteScene
Pastes the current scene from the clipboard without the pasted__ prefix.
This overrides the built in command for ctrl-v.
### Hotkeys
#### selectedChannelSetKey
Sets a key on the selected channels in the control box only.
### Hotkeys
#### toggleIsolateSelected
Toggles the state for the isolate selected in the current panel.
### Py
#### combine
Combines selected objects without destroying hierarchy and transforms.
### Py
#### copy_transform
Moves the selected object to the last selected object's position.
### Py
#### create_camera
Creates a camera from the current view in the active panel.
### Py
#### cube_unwrap
Unwrap them cube like objects by cutting all edges on one face and then unwrapping it like a box.
It will try to keep always one edge connected so it creates only one shell.
### Py
#### curve_tools
Curve tools to instance and place along curve
https://vimeo.com/209927561
### Py
#### cut_hard_edges
Cuts and unwraps objects based on hard edges.
### Py
#### extract_faces
Extract the currently selected faces from the object without separating different shells. Slow!
### Py
#### file_utils
A collections of file utility functions.
**import_files**
Import multiplie files and delete the mtl file when importing obj.

Args:
    remove_materials (boolean): Removes the .mtl files for .obj files. Default is True.

**export_selected**
Export selected to a specified temp directory as obj.

Args:
    path (string): Specify a path to export files to. Default is <project>/export
    single (boolean): If set will export each selected object to a separate file. Default is false.

**save_incremental**
Save version up when using the v000 version pattern for naming.
### Py
#### layout_uvs
Layout uvs grouped by objects and gap in between.

Args:
    gap (float): Gap between each group of uvs in uvspace.
### Py
#### merge_vertices
Merge vertices and display how many vertices have been merged.

Args:
    threshold (float): Distance threshold for merge operation.
### Py
#### mirror_patches
Mirrors the patches of selected UVs or all UVs on selected objects. Good with multiple UDIMs.
### Py
#### poly_smooth
Create duplicate mesh and apply subdivisions with all settings.
### Py
#### __init__
Apply random transformations to objects with live preview functionality.
### Py
#### remove_namespaces
Deletes all namespaces

Args:
    name (string): Specify namespace to be removed.
### Py
#### remove_shapes
Removes any additional shape nodes if an object has more than one.
### Py
#### __init__
Simple rename utility for batch renaming of objects.
### Py
#### rename_shadinggroups
Rename ShadingGroup nodes to match their incoming material.
### Py
#### select_bynormal
Selects faces by normal.

Args:
    angle (float): The angle in degrees that faces can face away from the selected face from.
    Default is 60.
### Py
#### select_hard_edges
Select hard edges.
### Py
#### select_nth_edge
Select every nth edge. Select two edges.
It will complete the edge ring with every nth edge selected.
### Py
#### set_pivot
Sets the translate pivot to the rotate/scale pivot.
### Py
#### transfer_uvs
Transfer UVs to multiple objects.
### Py
### Py
#### unwrap_objects
Unwraps the whole objects with Unfold 3d instead of having to select UVs.
