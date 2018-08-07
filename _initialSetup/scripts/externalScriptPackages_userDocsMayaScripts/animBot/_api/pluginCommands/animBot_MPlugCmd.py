




import sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


o__l__0 = 'animBot_MPlugCmd'


class o____o_____1___O____0___1(OpenMayaMPx.MPxCommand):

    def __init__(o____0__1_o):
        
        OpenMayaMPx.MPxCommand.__init__(o____0__1_o)

        o____0__1_o.o__O__O_l___O____o_l = OpenMaya.MDagModifier()

    def isUndoable(o____0__1_o):
        
        return True

    def doIt(o____0__1_o, args):
        

        from animBot._api.core import CORE

        o___l_____o___1_O_l____1_l = CORE.o___l_____o___1_O_l____1_l
        o____o___0__1_____0__l = OpenMaya.MFnNumericData()
        o___l__O____O = o____o___0__1_____0__l.create(OpenMaya.MFnNumericData.k2Float)
        o_____1___O____O____O_____1____o = [o___l_____O___o__l_0____l.o_1__O_o_l.asFloat() for o___l_____O___o__l_0____l in o___l_____o___1_O_l____1_l]

        
        for _o__0__l_O_O_____1____1_____1__O__1__0 in o___l_____o___1_O_l____1_l:
            o____0__1_o.o__O__O_l___O____o_l.newPlugValue(_o__0__l_O_O_____1____1_____1__O__1__0.o_1__O_o_l, o___l__O____O)

        try:
            o____0__1_o.o__O__O_l___O____o_l.doIt()
        except RuntimeError:
            
            pass

        
        for n, _o__0__l_O_O_____1____1_____1__O__1__0 in enumerate(o___l_____o___1_O_l____1_l):
            _o__0__l_O_O_____1____1_____1__O__1__0.setValue(o_____1___O____O____O_____1____o[n])


    def redoIt(o____0__1_o):
        
        o____0__1_o.o__O__O_l___O____o_l.doIt()

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


