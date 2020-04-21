from functools import partial

import maya.cmds as cmds

import zTools.rig.zbw_rig as rig
reload(rig)
import zbw_ikSpine_class
reload(zbw_ikSpine_class)
# get how many ctrls we want, then make curve have that many cvs
# refactor this out to functions - outputs for api style

# todo ---------- make this into a class, easier for the variable passing
#---------------- orient ctrls to match the vector we have
#----------------# setup FK controls? save for later
widgets = {}

def ikSpine_UI( *args):
    # name, base obj, top obj, num jnt
    if cmds.window("splineRigWin", exists=True):
        cmds.deleteUI("splineRigWin")

    widgets["win"] = cmds.window("splineRigWin")
    widgets["clo"] = cmds.columnLayout(w=300, h=150)

    widgets["nameTFG"] = cmds.textFieldGrp(l="Name:", cw=[(1, 50), (2, 200)], cal=[(1, "left"),(2, "left")], tx="spine")
    widgets["baseTFBG"] = cmds.textFieldButtonGrp(l="Base Obj:", cal=[(1, "left"),(2, "left"), (3, "left")], cw=[(1, 50), (2, 200), (3, 50)], bl="<<<", bc=partial(get_object, "baseTFBG"))
    widgets["endTFBG"] = cmds.textFieldButtonGrp(l="End Obj:", cal=[(1, "left"),(2, "left"), (3, "left")], cw=[(1, 50), (2, 200), (3, 50)], bl="<<<", bc=partial(get_object, "endTFBG"))
    widgets["numJntsIFG"] = cmds.intFieldGrp(l="Number of Joints:", cw=[(1, 100), (2, 50)], cal=[(1, "left"),(2, "left")], v1=20, cc=check_int_valid)
    widgets["midJntFFG"] = cmds.floatFieldGrp(l="Center Position:", cw=[(1, 100), (2,50)], cal=[(1, "left"), (2, "left")], v1=0.5, cc=check_float_valid)
    #option to NOT create tangents?
    widgets["executeBut"] = cmds.button(l="Create IK Spine Rig", bgc=(.5, .7, .5), h=40, w=300, c=collect_info)

    cmds.window(widgets["win"], e=True, w=5, h=5, rtf=True)
    cmds.showWindow(widgets["win"])


# HERE JUST CALL TO GET INFO OUT OF UI
def collect_info(*args):
    baseObj = cmds.textFieldButtonGrp(widgets["baseTFBG"], q=True, tx=True)
    endObj = cmds.textFieldButtonGrp(widgets["endTFBG"], q=True, tx=True)
    name = cmds.textFieldGrp(widgets["nameTFG"], q=True, tx=True)
    numJnts = cmds.intFieldGrp(widgets["numJntsIFG"], q=True, v1=True)
    midVal = cmds.floatFieldGrp(widgets["midJntFFG"], q=True, v1=True)

    if not baseObj or not endObj or not name:
        cmds.warning("Need to give me some info to work with!")
        return()

    if baseObj == endObj:
        cmds.warning("Can't have the same object as base and end!")
        return()

    basePos = cmds.xform(baseObj, ws=True, q=True, rp=True)
    endPos = cmds.xform(endObj, ws=True, q=True, rp=True)

# INSTEAD OF THIS, CALL THE CLASS
    rig = zbw_ikSpine_class.IKSpine(basePos, endPos, numJnts, name, midVal)

def check_int_valid(*args):
    num = cmds.intFieldGrp(widgets["numJntsIFG"], q=True, v1=True)
    if num < 3:
        cmds.intFieldGrp(widgets["numJntsIFG"], e=True, v1=3)


def check_float_valid(*args):
    num = cmds.floatFieldGrp(widgets["midJntFFG"], q=True, v1=True)
    if num < 0.0 or num > 1.0:
        cmds.warning("Value is from 0-1 (base-end)")
        cmds.floatFieldGrp(widgets["midJntFFG"], e=True, v1=.5)


def get_object(uiVal, *args):
    sel = cmds.ls(sl=True, l=True, type="transform")
    if sel:
        obj = sel[0]
        cmds.textFieldButtonGrp(widgets[uiVal], e=True, tx=obj)
    else: 
        cmds.warning("you need to select a transform!")


def ikSpine(*args):
    ikSpine_UI()