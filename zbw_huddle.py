########################
#file: zbw_huddle.py
#Author: zeth willie
#Contact: zeth@catbuks.com, www.williework.blogspot.com
#Date Modified: 04/27/13
#To Use: type in python window  "import zbw_huddle as hud; hud.huddle()"
#Notes/Descriptions:  Allows you to pick a pivot and the scale things closer to that, BUT not acutally scaling, but scaling the distance from that point
########################

import maya.cmds as cmds
import maya.OpenMaya as om

widgets = {}

def huddleUI(*args):
    """UI for the script"""

    if cmds.window("hudWin", exists=True):
        cmds.deleteUI("hudWin")

    widgets["win"] = cmds.window("hudWin", t="zbw_huddle", w=400, h=100)

    widgets["CLO"] = cmds.columnLayout()

    widgets["slider"] = cmds.floatSliderGrp(min=0, max=2, f=True, label="Huddle Scale Factor:", cal=([1, "left"], [2,"left"], [3,"left"]), cw=([1,100],[2,75],[3,225]), pre=3, v=1.0)
    cmds.separator(h=20)
    widgets["button"] = cmds.button(l="Move objects aroudnd first selected", w=200, h=50, bgc=(.6,.8, .6), c=huddleExec)

    cmds.showWindow(widgets["win"])
    cmds.window(widgets["win"], e=True, w=200, h=100)

def huddleExec(*args):
    """from first selection, will use vector math (basic addition/subtraction) to move the next selected objects closer or farther from first selection based on slider values (as a percentage)"""

    factor = cmds.floatSliderGrp(widgets["slider"], q=True, v=True)
    sel = cmds.ls(sl=True, type="transform")

    center = sel[0]

    objs = sel[1:]

    centerPos = cmds.xform(center, q=True, ws=True, rp=True)
    centerVec = om.MVector(centerPos[0], centerPos[1], centerPos[2])
    # print (centerVec[0], centerVec[1], centerVec[2])

    for obj in objs:
        # get location
        objPos = cmds.xform(obj, ws=True, q=True, rp=True)
        objVec = om.MVector(objPos[0], objPos[1], objPos[2])
        # print (objVec[0], objVec[1], objVec[2])

        #find difference vector between obj and center
        diffVec = objVec-centerVec
        #scale that vector
        scaledVec = diffVec * factor

        #add that vector to the center vec
        newVec = scaledVec + centerVec

        #apply it to the position of the obj
        cmds.xform(obj, ws=True, t=(newVec[0], newVec[1], newVec[2]))

def huddle(*args):
    """Use this to start the script!"""

    huddleUI()