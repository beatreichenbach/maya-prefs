# Sets a key on the selected channels in the control box.


from maya import cmds

def selectedChannelSetKey():
    attrs = cmds.channelBox('mainChannelBox', query=True, selectedMainAttributes=True) or []
    for attr in attrs:
        cmds.setKeyframe(attribute=attr)
