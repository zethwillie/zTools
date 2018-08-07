




import sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


o_____1_l___o____l_____0 = 'animBot_MPlugCmd'


class o____l____l____0____O___O__0_____O_0____1__O(OpenMayaMPx.MPxCommand):

    def __init__(o___o):
        
        OpenMayaMPx.MPxCommand.__init__(o___o)

        o___o.o___o_o____1___o = OpenMaya.MDagModifier()

    def isUndoable(o___o):
        
        return True

    def doIt(o___o, args):
        

        from animBot._api.core import CORE

        o_____o_____0___o = CORE.o_____o_____0___o
        o_____1____O_____0 = OpenMaya.MFnNumericData()
        o_____1___1_o_____o__l = o_____1____O_____0.create(OpenMaya.MFnNumericData.k2Float)
        o____0__l_O____O_1____l__0_____l = [o__0____O__1___1___1_____1_l__0_O_____l.o____1_0.asFloat() for o__0____O__1___1___1_____1_l__0_O_____l in o_____o_____0___o]

        
        for _o___0__O_l____1 in o_____o_____0___o:
            o___o.o___o_o____1___o.newPlugValue(_o___0__O_l____1.o____1_0, o_____1___1_o_____o__l)

        try:
            o___o.o___o_o____1___o.doIt()
        except RuntimeError:
            
            pass

        
        for n, _o___0__O_l____1 in enumerate(o_____o_____0___o):
            _o___0__O_l____1.setValue(o____0__l_O____O_1____l__0_____l[n])


    def redoIt(o___o):
        
        o___o.o___o_o____1___o.doIt()

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


