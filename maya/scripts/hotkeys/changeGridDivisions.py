# Halves or doubles the divisions on the viewport grid.
#
# Args:
#     change (int): Havles the number of divisions if set to -1. Doubles if set to 1.


from maya import cmds

def changeGridDivisions(change):
    current_divisions = cmds.grid(query=True, divisions=True)
    divisions = current_divisions * (2 ** change)
    cmds.grid(divisions=divisions)

    # status message
    units = cmds.grid(query=True, spacing=True) / divisions
    text = '{} Unit{}'.format(units, 's' if units != 1 else '')
    cmds.inViewMessage(
        statusMessage=text,
        position='topCenter',
        backColor='0x00000000',
        fade=True)
