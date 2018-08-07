




import sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


o_____1_l___o____l_____0 = 'animBot_MAnimCurveCmd'


class o____l____l____0____O___O__0_____O_0____1__O(OpenMayaMPx.MPxCommand):

    def __init__(o___o):
        
        OpenMayaMPx.MPxCommand.__init__(o___o)

        o___o.o___o_o____1___o = OpenMaya.MDagModifier()

    def isUndoable(o___o):
        
        return True

    def redoIt(o___o):
        

        from animBot._api.core import CORE

        if CORE.o___o_0___o == None:
            return

        o___o_0___o = CORE.o___o_0___o
        o___o.undoIt = o___o_0___o.undoIt
        o___o.redoIt = o___o_0___o.redoIt


    def doIt(o___o, args):
        
        return o___o.redoIt()

    def undoIt(o___o):
        
        o___o.o___o_o____1___o.undoIt()







def cmdCreator():
    
    return OpenMayaMPx.asMPxPtr(o____l____l____0____O___O__0_____O_0____1__O())


def initializePlugin(o____O_____1__l_____l_O_____0):
    
    o_O____o____O_0 = OpenMayaMPx.MFnPlugin(o____O_____1__l_____l_O_____0)
    try:
        o_O____o____O_0.registerCommand(o_____1_l___o____l_____0, cmdCreator)
    except:
        sys.stderr.write('Failed to register command: ' + o_____1_l___o____l_____0)


def uninitializePlugin(o____O_____1__l_____l_O_____0):
    
    o_O____o____O_0 = OpenMayaMPx.MFnPlugin(o____O_____1__l_____l_O_____0)
    try:
        o_O____o____O_0.deregisterCommand(o_____1_l___o____l_____0)
    except:
        sys.stderr.write('Failed to unregister command: ' + o_____1_l___o____l_____0)


