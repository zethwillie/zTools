########################
# file: zbw_tools.py
# Author: zeth willie
# Contact: zethwillie@gmail.com, www.williework.blogspot.com
# Date Modified: 8/17/17
# To Use: type in python window  "import zbw_tools as tools; reload(tools); tools.tools()"
# Notes/Descriptions: some rigging, anim, modeling and shading tools. *** requires zTools package in a python path.
########################

# TODO add some tooltips to buttons
# Todo - add docs to all of these

#TODO convert to windows class

from functools import partial
import os
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import importlib

import zTools.rig.zbw_rig as rig
reload(rig)
import zTools.resources.zbw_pipe as pipe
reload(pipe)
import zTools.resources.zbw_removeNamespaces as rmns
import zTools.resources.zbw_registeredTools as zReg
reload(zReg)


widgets = {}

# make sure maya can see and call mel scripts from zTools (where this is called from)
zToolsPath = os.path.dirname(os.path.abspath(__file__))
subpaths = ["", "rig", "resources", "anim", "model", "shaderRender",]
newPaths = []
for p in subpaths:
    thisPath = os.path.join(zToolsPath, p)
    newPaths.append(thisPath)

# set up these zTools paths for maya to recognize mel scripts
pipe.add_maya_script_paths(newPaths)

zRigDict = zReg.zRigDict
zAnimDict = zReg.zAnimDict
zModelDict = zReg.zModelDict
zShdDict = zReg.zShdDict

colors = rig.colors

def tools_UI(*args):
    if cmds.window("toolsWin", exists=True):
        cmds.deleteUI("toolsWin")

    widgets["win"] = cmds.window("toolsWin", t="zTools", w=280, rtf=True,
                                 s=True)
    widgets["tab"] = cmds.tabLayout(w=280)
    widgets["rigCLO"] = cmds.columnLayout("TD", w=280)
    widgets["rigFLO"] = cmds.formLayout(w=280, bgc=(0.1, 0.1, 0.1))

    # controls layout
    widgets["ctrlFLO"] = cmds.formLayout(w=270, h=50, bgc=(0.3, 0.3, 0.3))
    widgets["ctrlFrLO"] = cmds.frameLayout(l="CONTROLS", w=270, h=50, bv=True,bgc=(0.0, 0.0, 0.0))
    widgets["ctrlInFLO"] = cmds.formLayout(bgc=(0.3, 0.3, 0.3))
    widgets["ctrlAxisRBG"] = cmds.radioButtonGrp(l="Axis", nrb=3, la3=("x", "y", "z"),cw=([1, 33], [2, 33], [3, 33]),cal=([1, "left"], [2, "left"],[3, "left"]), sl=1)
    widgets["ctrlBut"] = cmds.button(l="Create", w=50, bgc=(.7,.7,.5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="circle", c=partial(control, "circle"))
    cmds.menuItem(l="sphere", c=partial(control, "sphere"))
    cmds.menuItem(l="square", c=partial(control, "square"))
    cmds.menuItem(l="star", c=partial(control, "star"))
    cmds.menuItem(l="cube", c=partial(control, "cube"))
    cmds.menuItem(l="lollipop", c=partial(control, "lollipop"))
    cmds.menuItem(l="barbell", c=partial(control, "barbell"))
    cmds.menuItem(l="cross", c=partial(control, "cross"))
    cmds.menuItem(l="bentCross", c=partial(control, "bentCross"))
    cmds.menuItem(l="arrow", c=partial(control, "arrow"))
    cmds.menuItem(l="bentArrow", c=partial(control, "bentArrow"))
    cmds.menuItem(l="arrowCross", c=partial(control, "arrowCross"))
    cmds.menuItem(l="splitCircle", c=partial(control, "splitCircle"))
    cmds.menuItem(l="cylinder", c=partial(control, "cylinder"))
    cmds.menuItem(l="octagon", c=partial(control, "octagon"))
    cmds.menuItem(l="halfCircle", c=partial(control, "halfCircle"))
    cmds.menuItem(l="arrowCircle", c=partial(control, "arrowCircle"))
    cmds.menuItem(l="arrowSquare", c=partial(control, "arrowSquare"))
    cmds.menuItem(l="4ArrowSquare", c=partial(control, "4arrowSquare"))
    cmds.menuItem(l="MASTER PACK", c=create_master_pack)
    
    widgets["swapBut"] = cmds.button(l="Swap", w=50, bgc=(.7,.5,.5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="circle", c=partial(swap, "circle"))
    cmds.menuItem(l="sphere", c=partial(swap, "sphere"))
    cmds.menuItem(l="square", c=partial(swap, "square"))
    cmds.menuItem(l="star", c=partial(swap, "star"))
    cmds.menuItem(l="cube", c=partial(swap, "cube"))
    cmds.menuItem(l="lollipop", c=partial(swap, "lollipop"))
    cmds.menuItem(l="barbell", c=partial(swap, "barbell"))
    cmds.menuItem(l="cross", c=partial(swap, "cross"))
    cmds.menuItem(l="bentCross", c=partial(swap, "bentCross"))
    cmds.menuItem(l="arrow", c=partial(swap, "arrow"))
    cmds.menuItem(l="bentArrow", c=partial(swap, "bentArrow"))
    cmds.menuItem(l="arrowCross", c=partial(swap, "arrowCross"))
    cmds.menuItem(l="splitCircle", c=partial(swap, "splitCircle"))
    cmds.menuItem(l="cylinder", c=partial(swap, "cylinder"))
    cmds.menuItem(l="octagon", c=partial(swap, "octagon"))
    cmds.menuItem(l="halfCircle", c=partial(swap, "halfCircle"))
    cmds.menuItem(l="arrowCircle", c=partial(swap, "arrowCircle"))
    cmds.menuItem(l="arrowSquare", c=partial(swap, "arrowSquare"))
    cmds.menuItem(l="4ArrowSquare", c=partial(swap, "4arrowSquare"))


    cmds.formLayout(widgets["ctrlInFLO"], e=True, af=[
        (widgets["ctrlAxisRBG"],"left", 0),
        (widgets["ctrlAxisRBG"], "top", 0),
        (widgets["ctrlBut"], "left", 170),
        (widgets["ctrlBut"], "top", 0),
        (widgets["swapBut"], "left", 220),
        (widgets["swapBut"], "top", 0),
    ])
    # TODO - add scale factor field for control creation

    # action layout
    cmds.setParent(widgets["rigFLO"])
    widgets["actionFLO"] = cmds.formLayout(w=280, h=330, bgc=(0.3, 0.3, 0.3))
    widgets["actionFrLO"] = cmds.frameLayout(l="ACTIONS", w=280, h=330, bv=True, bgc=(0, 0, 0))
    widgets["actionRCLO"] = cmds.rowColumnLayout(bgc=(0.3, 0.3, 0.3), nc=2)
    widgets["grpFrzBut"] = cmds.button(l="group freeze selected", w=140, bgc=(.5, .7, .5), c=group_freeze)
    widgets["selHier"] = cmds.button(l="sel hierarchy", w=140, bgc=(.5, .7, .5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="Select Full Hierarchy", c= select_hi)
    cmds.menuItem(l="Select Curve Hierarchy", c=partial(select_hierarchy, "curve"))
    cmds.menuItem(l="Select Joint Hierarchy", c=partial(select_hierarchy, "joint"))
    cmds.menuItem(l="Select Poly Hierarchy", c=partial(select_hierarchy, "poly"))
    widgets["grpCnctBut"] = cmds.button(l="group freeze + connect", w=140, bgc=(.5, .7, .5), c=freeze_and_connect)
    widgets["prntChnBut"] = cmds.button(l="parent chain selected", w=140, bgc=(.5, .7, .5), c=parent_chain)
    widgets["hideShp"] = cmds.button(l="sel shape vis toggle", w=140, bgc=(.5, .7, .5), c=hide_shape)
    widgets["bBox"] = cmds.button(l="bounding box control", w=140, bgc=(.5, .7, .5), c=bBox)
    widgets["cpSkinWtsBut"] = cmds.button(l="copy skin & weights", w=140, bgc=(.5, .7, .5), c=copy_skinning)
    widgets["remNSBut"] = cmds.button(l="remove all namespaces", w=140, bgc=(.5, .7, .5), c=remove_namespace)
    widgets["cntrLoc"] = cmds.button(l="sel vtx cntr jnt", w=140,bgc=(.5, .7, .5), c=center_joint)
    widgets["addToDef"] = cmds.button(l="add to deformer", w=140, bgc=(.5, .7, .5), c=add_to_deformer)
    widgets["snapto"] = cmds.button(l="snap B to A", w=140, bgc=(.5, .7, .5),c=snap_b_to_a)
    widgets["constrain"] = cmds.button(l="Create Constraint", w=140, bgc=(.5, .7, .5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="parent - maintain offset", c=partial(create_constraint, "prnt", True))
    cmds.menuItem(l="parent & scale - maintain offset", c=partial(create_constraint, "prntscl", True))
    cmds.menuItem(l="point & orient - maintain offset", c=partial(create_constraint, "pntornt", True))    
    cmds.menuItem(l="point - maintain offset", c=partial(create_constraint, "pnt", True))
    cmds.menuItem(l="orient - maintain offset", c=partial(create_constraint, "ornt", True))
    cmds.menuItem(l="scale - maintain offset", c=partial(create_constraint, "scl", True))
    cmds.menuItem(l="point - no offset", c=partial(create_constraint, "pnt", False))
    cmds.menuItem(l="orient - no offset", c=partial(create_constraint, "ornt", False))
    cmds.menuItem(l="parent - no offset", c=partial(create_constraint, "prnt", False))
    cmds.menuItem(l="scale - no offset", c=partial(create_constraint, "scl", False))
    #widgets["zeroPiv"] = cmds.button(l="Zero Pivot", w=140, bgc=(.5, .7, .5),c=zero_pivot)
    widgets["centerPiv"] = cmds.button(l="Pivot", w=140, bgc=(.5, .7, .5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="Center Pivot", c=center_pivot)
    cmds.menuItem(l="Snap pivots to last", c=snap_pivot)
    cmds.menuItem(l="Snap pivots to origin", c=zero_pivot)
    widgets["clnJntBut"] = cmds.button(l="Scrub Jnt Chain", w=140, bgc=(.5, .7, .5), c=clean_joints)
    widgets["createBut"] = cmds.button(l="Create: ", w=140, bgc=(.5, .7, .5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="joint", c=create_joint)
    cmds.menuItem(l="locator", c=create_locator)
    cmds.menuItem(l="set from sel", c=rig.create_set)
    cmds.menuItem(l="displayLayer from sel", c=rig.display_layer_from_selection)
    cmds.menuItem(l="zeroed cube", c=partial(zeroed_geo, "cube"))
    cmds.menuItem(l="zeroed cylinder", c=partial(zeroed_geo, "cylinder"))
    cmds.menuItem(l="zeroed cone", c=partial(zeroed_geo, "cone"))
    widgets["sftJntBut"] = cmds.button(l="Joint from softSel", w=140, bgc=(.5, .7, .5), c=partial(zAction, zRigDict, "softJoint"))
    widgets["invertBut"] = cmds.button(l="Invert Shape", w=140, bgc=(.5, .7, .5), c=invert_shape)
    widgets["hmmrBut"] = cmds.button(l="Hammer Weights", w=140, bgc=(.5, .7, .5), c=hammer_skin_weights)
    widgets["showHide"] = cmds.button(l="ShowHide", w=140, bgc=(.5, .7, .5))
    cmds.popupMenu(b=1)
    cmds.menuItem(l="Show all", c=partial(show_hide_in_panels, "showAll"))
    cmds.menuItem(l="Polys only", c=partial(show_hide_in_panels, "polys"))
    cmds.menuItem(l="Curves only", c=partial(show_hide_in_panels, "curves"))
    cmds.menuItem(l="Polys and curves only", c=partial(show_hide_in_panels, "polyCurve"))
    cmds.menuItem(l="Joints only", c=partial(show_hide_in_panels, "joints"))
    cmds.menuItem(l="Joints off", c=partial(show_hide_in_panels, "jointsOff"))
    widgets["selBindJnts"] = cmds.button(l="Sel Bind Jnts", w=140, bgc=(.5, .7, .5), c=select_bind_joints_from_geo)


    cmds.rowColumnLayout(w=140, nc=2, cs=[(1, 5), (2,5)])
    widgets["deleteH"] = cmds.button(l="del hist", w=65, bgc=(.7, .7, .5), c=partial(deleteH, 0))
    widgets["deleteAnim"] = cmds.button(l="del Anim", w=65, bgc=(.7, .5, .5), c=partial(deleteH, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=4, cs=[(1, 5), (2,5), (3,5), (4,5)])
    cmds.text("Freeze: ")
    widgets["freezeT"] = cmds.button(l="T", w=23, bgc=(.7, .5, .5), c=partial(freeze, 1, 0, 0))
    widgets["freezeR"] = cmds.button(l="R", w=23, bgc=(.5, .7, .5), c=partial(freeze, 0, 1, 0))
    widgets["freezeS"] = cmds.button(l="S", w=23, bgc=(.5, .5, .7), c=partial(freeze, 0, 0, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,10), (3, 5)])
    cmds.text("Curve Thick")
    widgets["linThkBut"] = cmds.button(l="-", w=30, bgc=(.7, .5, .5), c=partial(line_width, 0))
    widgets["linThnBut"] = cmds.button(l="+", w=30, bgc=(.5, .7, .5), c=partial(line_width, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,5), (3, 5)])
    cmds.text("Joint Draw ")
    widgets["jntDrwOn"] = cmds.button(l="off", w=30, bgc=(.7, .5, .5), c=partial(joint_draw, 2))
    widgets["jntDrwOff"] = cmds.button(l="on", w=30, bgc=(.5, .7, .5), c=partial(joint_draw, 0))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,17), (3, 5)])
    cmds.text("Joint Size ")
    widgets["jntSizeUp"] = cmds.button(l="-", w=30, bgc=(.7, .5, .5), c=partial(size_joints, 0))
    widgets["jntSizeDn"] = cmds.button(l="+", w=30, bgc=(.5, .7, .5), c=partial(size_joints, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.rowColumnLayout(w=140, nc=3, cs=[(1, 5), (2,8), (3, 5)])
    cmds.text("LocRotAxis")
    widgets["lraOff"] = cmds.button(l="off", w=30, bgc=(.7, .5, .5), c=partial(lra_toggle, 0))
    widgets["lraOn"] = cmds.button(l="on", w=30, bgc=(.5, .7, .5), c=partial(lra_toggle, 1))
    cmds.setParent(widgets["actionRCLO"])

    cmds.setParent(widgets["actionRCLO"])

#TODO -- add hide ai attributes
    # script Layout
    cmds.setParent(widgets["rigFLO"])
    widgets["zScrptFLO"] = cmds.formLayout(w=280, bgc=(0.3, 0.3, 0.3))
    widgets["zScrptFrLO"] = cmds.frameLayout(l="SCRIPTS", w=280, bv=True, bgc=(0.0, 0.0, 0.0))
    widgets["rigScriptsRCLO"] = cmds.rowColumnLayout(w=280, nc=2)
    widgets["attrBut"] = cmds.button(l="zbw_attrs", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "attr"))
    widgets["shpSclBut"] = cmds.button(l="zbw_shapeScale", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"shpScl"))
    widgets["selBufBut"] = cmds.button(l="zbw_selectionBuffer", w=140,bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"selBuf"))
    widgets["snapBut"] = cmds.button(l="zbw_snap", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "snap"))
    widgets["follBut"] = cmds.button(l="zbw_makeFollicle", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"foll"))
    widgets["jntRadBut"] = cmds.button(l="zbw_jointRadius", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"jntRadius"))
    widgets["typFindBut"] = cmds.button(l="zbw_typeFinder", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"typFind"))
    widgets["cmtRename"] = cmds.button(l="cometRename", w=140, bgc=(.5, .5, .5), c=partial(zMelAction, zRigDict, "cmtRename"))
    #widgets["abSym"] = cmds.button(l="abSymMesh", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict,"abSym"))
    widgets["cmtJntOrnt"] = cmds.button(l="cometJntOrient", w=140, bgc=(.5, .5, .5), c=partial(zMelAction, zRigDict,"cmtJntOrnt"))
    #widgets["extract"] = cmds.button(l="Extract Deltas", w=135, bgc=(.5, .5,.5), c=extract_deltas)

    # color layout
    cmds.setParent(widgets["rigFLO"])
    widgets["colorFLO"] = cmds.formLayout(w=280, h=66, bgc=(0.3, 0.3, 0.3))
    widgets["colorFrLO"] = cmds.frameLayout(l="COLORS", w=280, h=66, bv=True, bgc=(0.0, 0.0, 0.0))
    widgets["colorRCLO"] = cmds.rowColumnLayout(nc=6)
    widgets["redCNV"] = cmds.canvas(w=48, h=20, rgb=(1, 0, 0), pc=partial(changeColor, colors["red"]))
    widgets["pinkCNV"] = cmds.canvas(w=48, h=20, rgb=(1, .8, .965), pc=partial(changeColor, colors["pink"]))
    widgets["blueCNV"] = cmds.canvas(w=48, h=20, rgb=(0, 0, 1), pc=partial(changeColor, colors["blue"]))
    widgets["ltBlueCNV"] = cmds.canvas(w=48, h=20, rgb=(.65, .8, 1), pc=partial(changeColor, colors["lightBlue"]))
    widgets["greenCNV"] = cmds.canvas(w=48, h=20, rgb=(0, 1, 0), pc=partial(changeColor, colors["green"]))
    widgets["dkGreenCNV"] = cmds.canvas(w=48, h=20, rgb=(0, .35, 0), pc=partial(changeColor, colors["darkGreen"]))
    widgets["yellowCNV"] = cmds.canvas(w=48, h=20, rgb=(1, 1, 0), pc=partial(changeColor, colors["yellow"]))
    widgets["brownCNV"] = cmds.canvas(w=48, h=20, rgb=(.5, .275, 0), pc=partial(changeColor, colors["brown"]))
    widgets["purpleCNV"] = cmds.canvas(w=48, h=20, rgb=(.33, 0, .33), pc=partial(changeColor, colors["purple"]))
    widgets["dkPurpleCNV"] = cmds.canvas(w=48, h=20, rgb=(.15, 0, .25), pc=partial(changeColor, colors["darkPurple"]))
    widgets["dkRedCNV"] = cmds.canvas(w=48, h=20, rgb=(.5, .0, 0), pc=partial(changeColor, colors["darkRed"]))
    widgets["ltBrownCNV"] = cmds.canvas(w=48, h=20, rgb=(.7, .5, .0), pc=partial(changeColor, colors["lightBrown"]))
# ---------------- add three more colors
    # formlayout stuff
    cmds.formLayout(widgets["rigFLO"], e=True, af=[
        (widgets["ctrlFLO"], "left", 0),
        (widgets["ctrlFLO"], "top", 0),
        (widgets["actionFLO"], "left", 0),
        (widgets["actionFLO"], "top", 50),
        (widgets["zScrptFLO"], "left", 0),
        (widgets["zScrptFLO"], "top", 457),
        (widgets["colorFLO"], "left", 0),
        (widgets["colorFLO"], "top", 385),
    ])

    cmds.setParent(widgets["tab"])
    widgets["rigsCLO"] = cmds.columnLayout("RIGS", w=280)
    widgets["rigsPropFrameLO"] = cmds.frameLayout(l="PROP RIGGING", w=280, bv=True, bgc=(0, 0, 0))
    widgets["rigsPropRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["sftDefBut"] = cmds.button(l="Soft Deformers", w=140, bgc=(.7, .5, .5), c=partial(zAction,zRigDict,"softMod"))
    widgets["RcrvTools"] = cmds.button(l="Curve Tools", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "crvTools"))
    widgets["smIKBut"] = cmds.button(l="Single Jnt IK", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"smIK"))
    widgets["autoSqBut"] = cmds.button(l="AutoSquash Rig", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"autoSquash"))
    widgets["wireBut"] = cmds.button(l="Wire Def Rig", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "wire"))

    cmds.setParent(widgets["rigsCLO"])
    widgets["rigsCharFrameLO"] = cmds.frameLayout(l="CHARACTER RIGGING", w=280, bv=True, bgc=(0, 0, 0))
    widgets["rigsCharRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["legBut"] = cmds.button(l="Leg Rig", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"leg"))
    widgets["armBut"] = cmds.button(l="Arm Rig", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "arm"))
    
    cmds.setParent(widgets["rigsCLO"])
    widgets["rigsCharTFrameLO"] = cmds.frameLayout(l="CHARACTER TOOLS", w=280, bv=True, bgc=(0, 0, 0))
    widgets["rigsCharTRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["ribBut"] = cmds.button(l="Ribbon Rig", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"ribbon"))
    widgets["splineBut"] = cmds.button(l="Spline IK Rig", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "splineIK"))
    widgets["followBut"] = cmds.button(l="Follow Constraints", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"follow"))
    widgets["mgRig"] = cmds.button(l="spherical Crv Rig", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "sphereCrvRig"))


    cmds.setParent(widgets["tab"])
    widgets["modelLgtCLO"] = cmds.columnLayout("MDL_LGT", w=280)
# curve tools, model scripts, add to lattice, select hierarchy, snap selection buffer, transform buffer
    widgets["mdlMdlFrameLO"] = cmds.frameLayout(l="MODELING", w=280, bv=True, bgc=(0, 0, 0))
    widgets["mdlPropRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["MaddToLat"] = cmds.button(l="add to deformer", w=140, bgc=(.5, .7, .5), c=add_to_deformer)
    #widgets["extend"] = cmds.button(l="zbw_polyExtend", w=140, bgc=(.7, .5, .5),c=partial(zAction, zModelDict,"extend"))
    widgets["wrinkle"] = cmds.button(l="zbw_wrinklePoly", w=140, bgc=(.7, .5, .5), c=partial(zAction, zModelDict,"wrinkle"))
    widgets["McrvTools"] = cmds.button(l="zbw_curveTools", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "crvTools"))
    widgets["MtrnBuffer"] = cmds.button(l="zbw_transformBuffer", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "trfmBuffer"))
    widgets["MrandomSel"] = cmds.button(l="zhw_randomSel", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict,"randomSel"))
    widgets["MselBufBut"] = cmds.button(l="zbw_selectionBuffer", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict,"selBuf"))
    widgets["MsnapBut"] = cmds.button(l="zbw_snap", w=140, bgc=(.7, .5, .5), c=partial(zAction, zRigDict, "snap"))
    #widgets["MabSym"] = cmds.button(l="abSymMesh", w=140, bgc=(.5, .5, .5), c=partial(zAction, zRigDict,"abSym"))
    widgets["McmtRename"] = cmds.button(l="cometRename", w=140, bgc=(.5, .5, .5), c=partial(zMelAction, zRigDict,"cmtRename"))
    widgets["cube"] = cmds.button(l="zeroed cube", w=140, bgc=(.5, .7, .5), c= partial(zeroed_geo, "cube"))
    widgets["cylinder"] = cmds.button(l="zeroed cylinder", w=140, bgc=(.5, .7, .5), c=partial(zeroed_geo, "cylinder"))

    cmds.setParent(widgets["modelLgtCLO"])
    widgets["lgtFrameLO"] = cmds.frameLayout(l="LIGHTING RENDER", w=280, bv=True, bgc=(0, 0, 0))
    widgets["lgtPropRCLO"] = cmds.rowColumnLayout(nc=2, bgc=(0.3, 0.3, 0.3))
    widgets["transfer"] = cmds.button(l="zbw_shadingTransfer", w=140, bgc=(.7, .5, .5), c=partial(zAction, zShdDict, "shdTransfer"))
    widgets["previsShd"] = cmds.button(l="zbw_previsShaders", w=140, bgc=(.7, .5, .5), c=partial(zAction, zShdDict, "prvsShd"))    

    cmds.setParent(widgets["tab"])
    widgets["animCLO"] = cmds.columnLayout("ANIM", w=280)
    widgets["tween"] = cmds.button(l="tween machine", w=140, bgc=(.5, .5, .5), c=partial(zAction, zAnimDict, "tween"))
    widgets["noise"] = cmds.button(l="zbw_animNoise", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "noise"))
    widgets["audio"] = cmds.button(l="zbw_audioManager", w=140, bgc=(.7, .5, .5),c=partial(zAction, zAnimDict, "audio"))
    widgets["clean"] = cmds.button(l="zbw_cleanKeys", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "clean"))
    widgets["dupe"] = cmds.button(l="zbw_dupeSwap", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "dupe"))
    widgets["huddle"] = cmds.button(l="zbw_huddle", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict,"huddle"))
    widgets["randomSel"] = cmds.button(l="zhw_randomSel", w=140, bgc=(.7, .5, .5),c=partial(zAction, zAnimDict,"randomSel"))
    widgets["randomAttr"] = cmds.button(l="zbw_randomAttr", w=140, bgc=(.7, .5, .5),c=partial(zAction, zAnimDict,"randomAttr"))
    widgets["clip"] = cmds.button(l="zbw_setClipPlanes", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict,"clip"))
    widgets["tangents"] = cmds.button(l="zbw_tangents", w=140, bgc=(.7, .5, .5), c=partial(zAction, zAnimDict, "tangents"))
    widgets["studLib"] = cmds.button(l="Studio Library", w=140, bgc=(.5, .5,.5), c=partial(zAction, zAnimDict, "studioLib"))
    widgets["atools"] = cmds.button(l="animBot", w=140, bgc=(.5, .5,.5), c=partial(zAction, zAnimDict, "animBot"))


    cmds.setParent(widgets["tab"])
    widgets["lgtRndCLO"] = cmds.columnLayout("MISC", w=280)
    widgets["saveScrpt"] = cmds.button(l="save script win", w=140, bgc=(.7, .5, .5), c=save_script_win)
    widgets["monWin"] = cmds.button(l="window cleanup", w=140, bgc=(.7, .5, .5))



    cmds.window(widgets["win"], e=True, rtf=True, w=5, h=5)
    cmds.showWindow(widgets["win"])

##########
# functions
##########

def control(type="none", *args):
    """
    gets the name from the button pushed and the axis from the radio button group
    and creates a control at the origin
    """
    axisRaw = cmds.radioButtonGrp(widgets["ctrlAxisRBG"], q=True, sl=True)
    if axisRaw == 1:
        axis = "x"
    if axisRaw == 2:
        axis = "y"
    if axisRaw == 3:
        axis = "z"

    rig.create_control(name="Ctrl", type=type, axis=axis, color="yellow")


def swap(type="none", *args):
    axisRaw = cmds.radioButtonGrp(widgets["ctrlAxisRBG"], q=True, sl=True)
    if axisRaw == 1:
        axis = "x"
    if axisRaw == 2:
        axis = "y"
    if axisRaw == 3:
        axis = "z"

    rig.swap_shape(type=type, axis=axis, scale=1.0, color=None)


# change below to become a dynmaic import: action[0] should be just import, action[1] should be function call
# i.e. instead of exec(x), should be import dict[action[0]]; reload dict[action[0]; dict[action[0]].dict[action[1]]

def zAction(dic=None, action=None, *args):
    """
    grabs the action key from the given dictionary
    then imports the first value (module), reloads it
    then gets the function from the second value and runs that 
    """
    if action and dic:
        funcName = dic[action][1]
        mod = importlib.import_module(dic[action][0])
        reload(mod)
        func =  getattr(mod, funcName)
        func()

    else:
        cmds.warning(
            "zbw_tools.zAction: There was a problem with either the key or the dictionary given! (key: {0}, "
            "action: {1}".format(action, dic))


def zMelAction(dic=None, action=None, *args):
    """calls mel cmd from dict, and evals it"""
    print dic[action][0]
    mel.eval(dic[action][0])


def snap_b_to_a(*args):
    """
    snaps 2nd selection to 1st, translate and rotate. Transforms only
    """
    sel = cmds.ls(sl=True, type="transform")
    if sel and len(sel) > 1:
        src = sel[0]
        tgt = sel[1:]
        for t in tgt:
            rig.snap_to(src, t)


def invert_shape(*args):
    # assign a shader to this. . .
    cmds.invertShape()


def zero_pivot(*args):
    """puts pivots zeroed at origin"""
    sel = cmds.ls(sl=True, transforms=True)
    rig.zero_pivot(sel)


def clean_joints(*args):
    sel = cmds.ls(sl=True, type="joint")
    if sel:
        jnt = sel[0]
        rig.clean_joint_chain(jnt)
        cmds.joint(jnt, edit=True, orientJoint="xyz", secondaryAxisOrient="yup", ch=True)


def freeze(t=1, r=1, s=1, *args):
    sel = cmds.ls(sl=True)
    cmds.makeIdentity(sel, t=t, r=r, s=s, apply=True )


def deleteH(mode, *args):
    sel = cmds.ls(sl=True)
    if mode == 0:
        cmds.delete(sel, ch=True)
    else:
        cmds.delete(sel, c=True, timeAnimationCurves=True, unitlessAnimationCurves=False)


def zeroed_geo(gtype, *args):
    geo = None
    if gtype == "cube":
        geo = cmds.polyCube()
        cmds.xform(geo, ws=True, t=(0, .5, 0))
        cmds.xform(geo, ws=True, piv=(0,0,0))
    if gtype == "cylinder":
        geo = cmds.polyCylinder()
        cmds.xform(geo, ws=True, t=(0, 1, 0))
        cmds.xform(geo, ws=True, piv=(0,0,0))
    if gtype == "cone":
        geo = cmds.polyCone()
        cmds.xform(geo, ws=True, t=(0, 1, 0))
        cmds.xform(geo, ws=True, piv=(0,0,0))        
    cmds.select(geo, r=True)
    freeze()


def save_script_win(*args):
    mel.eval("syncExecuterBackupFiles")


def line_width(mode, *args):
    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            if rig.type_check(obj, "nurbsCurve"):
                shps = cmds.listRelatives(obj, s=True)
                if shps:
                    for shp in shps:
                        val = cmds.getAttr("{0}.lineWidth" .format(shp))
                        if mode == 0:
                            if val <= 1:
                                continue
                            else:
                                val -= 0.5
                        elif mode == 1:
                            if val <= 1:
                                val = 1.5
                            else:
                                val += 0.5
                        cmds.setAttr("{0}.lineWidth".format(shp), val)


def joint_draw(value, *args):
    jnts = cmds.ls(type="joint")
    for jnt in jnts:
        cmds.setAttr("{0}.drawStyle".format(jnt), value)


def size_joints(mode, *args):
    jnts = cmds.ls(type="joint")
    for jnt in jnts:
        jntRad = cmds.getAttr("{0}.radius".format(jnt))
        if mode == 0:
            jntRad *= 0.5
        elif mode == 1:
            jntRad *= 1.5

        if jntRad < 0.01:
            jntRad = 0.01
        cmds.setAttr("{0}.radius".format(jnt), jntRad)


def lra_toggle(value, *args):
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr("{0}.displayLocalAxis".format(obj), value)


def center_pivot(*args):
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.xform(obj, cp=True, p=True)


def snap_pivot(*args):
    sel = cmds.ls(sl=True)

    if not sel or len(sel)==1:
        return()

    src = sel[-1]
    tgts = sel[:-1]

    pos = cmds.xform(src, q=True, ws=True, rp=True)
    for tgt in tgts:
        cmds.xform(tgt, ws=True, piv=pos)


def show_hide_in_panels(objs, *args):
    """polys, curves, joints, jointsOff, polyCurve, showAll"""
    panels = cmds.getPanel(type="modelPanel")
    for p in panels:
        if objs == "polys" or objs=="curves" or objs=="joints" or objs == "polyCurve":
            cmds.modelEditor(p, e=True, allObjects=False)
        if objs == "polys" or objs=="polyCurve":
            cmds.modelEditor(p, e=True, polymeshes=True)
        if objs == "curves" or objs == "polyCurve":
            cmds.modelEditor(p, e=True, nurbsCurves=True)
        if objs == "joints":
            cmds.modelEditor(p, e=True, joints=True)
        if objs == "jointsOff":
            cmds.modelEditor(p, e=True, joints=False)
        if objs == "showAll":
            cmds.modelEditor(p, e=True, allObjects=True)


def create_joint(*args):
    cmds.select(cl=True)
    cmds.joint()


def create_master_pack(self):
    mst1 = rig.create_control(name="master_CTRL", type="arrowCircle", axis="y", color = "green")
    mst2 = rig.create_control(name="master_sub1_CTRL", type="circle", axis = "y", color = "darkGreen")
    mst2Grp = rig.group_freeze(mst2)
    mst3 = rig.create_control(name="master_sub2_CTRL", type="circle", axis = "y", color = "yellowGreen")
    mst3Grp = rig.group_freeze(mst3)

    rig.scale_nurbs_control(mst1, 3, 3, 3, origin=True)
    rig.scale_nurbs_control(mst2, 2.5, 2.5, 2.5)
    rig.scale_nurbs_control(mst3, 2, 2, 2)

    cmds.parent(mst3Grp, mst2)
    cmds.parent(mst2Grp, mst1)

    geoGrp = cmds.group(empty=True, name = "GEO")
    geoNoXform = cmds.group(empty=True, name="GEO_noTransform")
    geoXform = cmds.group(empty=True, name="GEO_transform")

    rigGrp = cmds.group(empty=True, name = "RIG")
    rigNoXform = cmds.group(empty=True, name="RIG_noTransform")
    rigXform = cmds.group(empty=True, name="RIG_transform")   

    cmds.parent([geoXform, geoNoXform], geoGrp)
    cmds.parent([rigNoXform, rigXform], rigGrp)
    cmds.parent([geoGrp, rigGrp], mst3)


def extract_deltas(*args):
    # check plug is loaded
    rig.plugin_load("extractDeltas")
    mel.eval("performExtractDeltas")


def parent_scale_constrain(*args):
    """ just creates a parent and scale transform on the tgt object """
    sel = cmds.ls(sl=True, type="transform")
    if not (sel and len(sel) == 2):
        cmds.warning("You need to select two tranform objects!")
        return ()
    src = sel[0]
    tgt = sel[1]
    cmds.parentConstraint(src, tgt, mo=True)
    cmds.scaleConstraint(src, tgt)


def remove_namespace(*args):
    """removes namespaces . . . """
    ns = rmns.remove_namespaces()
    if ns:
        print "Removed namespaces: ", ns
    else:
        print "Did not delete any namespaces!"


def add_to_deformer(*args):
    """
    select lattice then geo to add to the lattice
    """
    sel = cmds.ls(sl=True)
    if len(sel)<2:
        cmds.warning("Need to select the deformer, then some geometry")
        return()
    deformer = sel[0]
    geo = sel[1:]
    rig.add_geo_to_deformer(deformer, geo)


def group_freeze(*args):
    """group freeze an obj"""

    sel = cmds.ls(sl=True, type="transform")
    for obj in sel:
        rig.group_freeze(obj)


def select_hierarchy(sType, *args):
    """
        select top node(s) and this will (inclusively) select all the xforms below it of the given type ('curve', 'poly', 'joint')
    """
    sel = cmds.ls(sl=True, type="transform")
    selectList = []

    for top in sel:
        xforms = []
        cshps = None
        if sType == "curve":
            cshps = cmds.listRelatives(top, allDescendents=True , f=True, type="nurbsCurve")
        elif sType == "poly":
            cshps = cmds.listRelatives(top, allDescendents=True , f=True, type="mesh")
        if cshps:
            for cshp in cshps:
                xf = cmds.listRelatives(cshp, p=True, f=True)[0]
                xforms.append(xf)
        elif sType == "joint":
            jnts = cmds.listRelatives(top, allDescendents=True, f=True, type="joint")
            xforms = jnts

        if xforms:
            # sort list by greatest number of path splits first (deepest)
            xforms.sort(key=lambda a: a.count("|"), reverse=True)
            list(set(xforms))
            for x in xforms:
                selectList.append(x)

    cmds.select(selectList, r=True)


def freeze_and_connect(*args):
    sel = cmds.ls(sl=True)
    ctrlOrig = sel[0]
    grpList = []
    ctrlList = []

    for x in range(1, len(sel)):

        pos = cmds.xform(sel[x], ws=True, q=True, rp=True)
        rot = cmds.xform(sel[x], ws=True, q=True, ro=True)

        ctrl = cmds.duplicate(ctrlOrig, n="{}Ctrl".format(sel[x]))[0]
        grp = rig.group_freeze(ctrl)

        rig.snap_to(sel[x], grp)
        cmds.parentConstraint(ctrl, sel[x])
        grpList.append(grp)
        ctrlList.append(ctrl)
    
    zipList = zip(sel[1:], grpList, ctrlList)

    for i in range(len(zipList)):
        parID = None
        par = cmds.listRelatives(zipList[i][0], p=True)
        if par:
            try:
                parID = sel.index(par[0])-1
                parCtrl = zipList[parID][2]
                cmds.parent(zipList[i][1], parCtrl)
            except:
                pass

    cmds.delete(sel[0])


def parent_chain(*args):
    # parent chain (select objs, child first. WIll parent in order selected)

    sel = cmds.ls(sl=True)
    sizeSel = len(sel)
    for x in range(0, sizeSel - 1):
        cmds.parent(sel[x], sel[x + 1])


def select_hi(*args):
    cmds.select(hi=True)


def select_components(*args):
    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            shape = cmds.listRelatives(obj, s=True)[0]

            if cmds.objectType(shape) == "nurbsCurve":
                cmds.select(cmds.ls("{}.cv[*]".format(obj), fl=True))
            elif cmds.objectType(shape) == "mesh":
                cmds.select(cmds.ls("{}.vtx[*]".format(obj), fl=True))
            else:
                return


def hammer_skin_weights(*args):
    mel.eval("weightHammerVerts")


def create_locator(*args):
    cmds.spaceLocator()


def changeColor(color, *args):
    """change shape color of selected objs"""

    sel = cmds.ls(sl=True)

    if sel:
        for obj in sel:
            shapes = cmds.listRelatives(obj, s=True)
            if shapes:
                for shape in shapes:
                    cmds.setAttr("%s.overrideEnabled" % shape, 1)
                    cmds.setAttr("%s.overrideColor" % shape, color)


def create_constraint(ctype, offset=True, *args):
    sel = cmds.ls(sl=True, type="transform")
    if len(sel)<2:
        return()
    if "prnt" in ctype:
        cmds.parentConstraint( mo=offset)
    if "pnt" in ctype:
        cmds.pointConstraint(mo=offset)
    if "ornt" in ctype:
        cmds.orientConstraint(mo=offset)
    if "scl" in ctype:
        cmds.scaleConstraint(mo=offset)


def select_bind_joints_from_geo(*args):
    """selects bind joints from selected geo"""
    jnts = rig.get_bind_joints_from_geo()
    cmds.select(jnts, r=True)


def copy_skinning(*args):
    """select the orig bound mesh, then the new unbound target mesh and run"""

    sel = cmds.ls(sl=True)
    orig = sel[0]
    targets = sel[1:]

    for target in targets:
        try:
            jnts = cmds.skinCluster(orig, q=True, influence=True)
        except:
            cmds.warning("couldn't get skin weights from {}".format(orig))
        try:
            targetClus = cmds.skinCluster(jnts, target, bindMethod=0, skinMethod=0,normalizeWeights=1, maximumInfluences=3,obeyMaxInfluences=False, tsb=True)[0]
        except:
            cmds.warning("couln't bind to {}".format(target))
        origClus = mel.eval("findRelatedSkinCluster " + orig)
        # copy skin weights from orig to target
        try:
            cmds.copySkinWeights(ss=origClus, ds=targetClus, noMirror=True,
                                 sa="closestPoint", ia="closestJoint")
        except:
            cmds.warning("couldn't copy skin weights from {0} to {1}".format(orig, target))


def center_joint(*args):
    """creates a center loc on the avg position"""

# TODO -------- differentiate if these are objs or points
    sel = cmds.ls(sl=True, fl=True)
    if sel:
        ps = []
        for vtx in sel:
            ps.append(cmds.pointPosition(vtx))

        # this is cool!
        center = rig.average_vectors(ps)
        cmds.select(cl=True)
        jnt = cmds.joint(name="center_JNT")
        cmds.xform(jnt, ws=True, t=center)


def hide_shape(*args):
    """toggels the vis of the shape nodes of the selected objects"""

    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            shp = cmds.listRelatives(obj, shapes=True)
            if shp:
                for s in shp:
                    if cmds.getAttr("{}.visibility".format(s)):
                        cmds.setAttr("{}.visibility".format(s), 0)
                    else:
                        cmds.setAttr("{}.visibility".format(s), 1)


def bBox(*args):
    """creates a control based on the bounding box"""
    sel = cmds.ls(sl=True, type="transform")
    if sel:
        rig.bounding_box_ctrl(sel)


##########
# load function
##########

def tools(*args):
    tools_UI()
