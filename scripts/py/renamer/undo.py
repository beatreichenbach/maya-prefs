from functools import wraps
from maya import cmds
import logging


def undo(func):
    @wraps(func)
    def _undofunc(*args, **kwargs):
        try:
            cmds.undoInfo(openChunk=True)
            return func(*args, **kwargs)
        except Exception as e:
            cmds.undoInfo(closeChunk=True)
            logging.error(e)
            cmds.undo()
        else:
            cmds.undoInfo(closeChunk=True)

    return _undofunc
