# Merge vertices and display how many vertices have been merged.
#
# Args:
#     threshold (float): Distance threshold for merge operation.

from maya import cmds


def merge_vertices(threshold):
    selection = cmds.ls(selection=True)
    for s in selection:
        n = cmds.polyEvaluate(s, vertex=True)
        cmds.polyMergeVertex(s, distance=threshold)
        merged = (n - cmds.polyEvaluate(s, vertex=True))
        cmds.inViewMessage(
            statusMessage='{} Vertice{} merged'.format(merged, 's'[merged == 1:]),
            pos='topCenter',
            fade=True)
