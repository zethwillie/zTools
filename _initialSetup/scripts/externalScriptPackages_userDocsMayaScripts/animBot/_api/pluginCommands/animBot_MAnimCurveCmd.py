




import sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


o__l__0 = 'animBot_MAnimCurveCmd'


class o____o_____1___O____0___1(OpenMayaMPx.MPxCommand):

    def __init__(o____0__1_o):
        
        OpenMayaMPx.MPxCommand.__init__(o____0__1_o)

        o____0__1_o.o__O__O_l___O____o_l = OpenMaya.MDagModifier()

    def isUndoable(o____0__1_o):
        
        return True

    def redoIt(o____0__1_o):
        

        from animBot._api.core import CORE

        if CORE.o__O_0 == None:
            return

        o__O_0 = CORE.o__O_0
        o____0__1_o.undoIt = o__O_0.undoIt
        o____0__1_o.redoIt = o__O_0.redoIt


    def doIt(o____0__1_o, args):
        
        return o____0__1_o.redoIt()

    def undoIt(o____0__1_o):
        
        o____0__1_o.o__O__O_l___O____o_l.undoIt()







def cmdCreator():
    
    return OpenMayaMPx.asMPxPtr(o____o_____1___O____0___1())


def initializePlugin(o____0):
    
    o___0__O___1___0___l_____O_o = OpenMayaMPx.MFnPlugin(o____0)
    try:
        o___0__O___1___0___l_____O_o.registerCommand(o__l__0, cmdCreator)
    except:
        sys.stderr.write('Failed to register command: ' + o__l__0)


def uninitializePlugin(o____0):
    
    o___0__O___1___0___l_____O_o = OpenMayaMPx.MFnPlugin(o____0)
    try:
        o___0__O___1___0___l_____O_o.deregisterCommand(o__l__0)
    except:
        sys.stderr.write('Failed to unregister command: ' + o__l__0)


