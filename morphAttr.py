import maya.cmds as cmds
import maya.mel as mel


def morphAttrDo(*args):
    print "in morph attr do"
    if not cmds.selectPref(q=True, trackSelectionOrder=True):
        cmds.selectPref(trackSelectionOrder=True)
    
    sel = cmds.ls(orderedSelection=True)
    
    if not sel or len(sel)<3:
        cmds.warning("You need to select a sequence of objects!")
        return()

    chnls = getChannels()

    if not chnls:
        cmds.warning("You need to select a channel in the channelbox!")
        return()
        
    first = sel[0]
    last = sel[-1]

    for c in chnls:
        firstVal = cmds.getAttr("{0}.{1}".format(first, c))
        lastVal = cmds.getAttr("{0}.{1}".format(last, c))

        diff = lastVal-firstVal
        incr = diff/len(sel[1:])

        x = 1
        for obj in sel[1:-1]:
            cmds.setAttr("{0}.{1}".format(obj,c), (x*incr))
            x += 1


def getChannels(*args):
    cBox = mel.eval('$temp=$gChannelBoxName')
    cAttrs = cmds.channelBox(cBox, q=True, selectedMainAttributes=True, ssa=True, sha=True, soa=True)
    return cAttrs


def morphAttr(*args):
    morphAttrDo()