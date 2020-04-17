from functools import partial

import maya.cmds as cmds

import zTools.rig.zbw_rig as rig
reload(rig)
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


def check_int_valid(*args):
    num = cmds.intFieldGrp(widgets["numJntsIFG"], q=True, v1=True)
    if num < 3:
        cmds.intFieldGrp(widgets["numJntsIFG"], e=True, v1=3)


def check_float_valid(*args):
    num = cmds.floatFieldGrp(widgets["midJntFFG"], q=True, v1=True)
    if num < 0.0 or num > 1.0:
        cmds.warning("Value is from 0-1 (base-end)")
        cmds.floatFieldGrp(widgets["midJntFFG"], e=True, v1=.5)


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

    create_ikspline_rig(basePos, endPos, numJnts, name, midVal)


def get_object(uiVal, *args):
    sel = cmds.ls(sl=True, l=True, type="transform")
    if sel:
        obj = sel[0]
        cmds.textFieldButtonGrp(widgets[uiVal], e=True, tx=obj)


def create_ikspline_rig(basePos, endPos, numJnts, name="ikSpline", midVal=0.5):
    name = name

    #create joints
    jntList = create_joint_chain(name, basePos, endPos, numJnts)
    #create ik spline
    splHandle, splEffector, splCrv = create_ik_spline(name, jntList[0], jntList[-1])
    #create control joints
    ctrlJnts = create_control_joints(basePos, endPos, name)
    #create tangent joints
    tanJnts = create_tangent_joints(basePos, endPos, name, midVal)
    # create controls for control joints
    ctrlJntCtrls = create_controls(ctrlJnts, "CTRL", "y", "box", "yellow")
    topCtrl = ctrlJntCtrls[2][0]
    create_attributes(topCtrl)
    # create controls for tangents
    tanJntCtrls = create_controls(tanJnts, "CTRL", "y", "star", "darkPurple")
# separate function to setup tangents and constrain to mid, this is getting too messy
    #parent tangents in
    cmds.parent(tanJntCtrls[0][1], ctrlJntCtrls[0][0]) 
    cmds.parent(tanJntCtrls[1][1], ctrlJntCtrls[2][0]) 
    # tan0PC = cmds.parentConstraint(ctrlJntCtrls[0][0],tanJntCtrls[0][1], mo=True)
    # tan1PC = cmds.parentConstraint(ctrlJntCtrls[2][0],tanJntCtrls[1][1], mo=True)
    # attach controls to ctrl joints
    ctrlPCs = constrain_joints(ctrlJntCtrls, ctrlJnts)
    tanPCs = constrain_joints(tanJntCtrls, tanJnts)
    midPtC = cmds.pointConstraint(tanJnts, ctrlJntCtrls[1][1])
    midOC = cmds.orientConstraint(tanJnts, ctrlJntCtrls[1][1])
    # bind ctrl joints to curve
    bind_skin(ctrlJnts, splCrv)
    # setup twist on ik spline
    setup_spline_advanced_twist(splHandle, ctrlJntCtrls[0][0], ctrlJntCtrls[2][0], 0, 3)

    # setup attributes (use tangents, midFollowpos, orient), clean up rig, check bind weights
    measureCrv = setup_scaling(name, splCrv, jntList, topCtrl)
    connect_attributes(name, topCtrl, tanJntCtrls, midOC, midPtC)
    clean_up()
    return()
#---------------- deal with end jnt flipping (add a joint/s at the postion of the "B" jnt)
#---------------- squash and stretch on a ramp which tells where the effect takes place along the curve (ie. move joints up and down curve?)

    finalCtrlGrp = cmds.group(em=True, name="{0}_driverCtrl_GRP".format(name))
    cmds.parent(bindGrps, finalCtrlGrp)
    xformGrp = cmds.group(em=True, name="{0}_transform_GRP".format(name))
    cmds.parent([finalCtrlGrp, measureCrv, jntList[0]], xformGrp)
    noXformGrp = cmds.group(em=True, name="{0}_noTransform_GRP".format(name))
    cmds.parent([splCrv, splHandle], noXformGrp)

    hide = [measureCrv, splCrv, splHandle]
    for obj in hide:
        cmds.setAttr("{0}.v".format(obj), 0)

    # return the things (grps, ctrls, offset grps, etc)

def create_attributes(ctrl):
    cmds.addAttr(ctrl, ln="auto_stretch", at="double", min=0, max=1, k=True, dv=0)
    cmds.addAttr(ctrl, ln="tangents", at="double", min=0, max=1, k=True, dv=1)
    cmds.addAttr(ctrl, ln="midFollowsPosition", at="double", min=0, max=1, k=True, dv=1)
    cmds.addAttr(ctrl, ln="midFollowsRotation", at="double", min=0, max=1, k=True, dv=1)


def create_ik_spline(name, startJnt, endJnt):
#----------------check setting here, crv should have 3 or 4 spans?  Root twist mode   
    splHandle, splEffector, splCrv = cmds.ikHandle(startJoint=startJnt, ee=endJnt, sol="ikSplineSolver", numSpans=2, rootTwistMode=True, parentCurve=False, name="{0}_IK".format(name))
    splCrv = cmds.rename(splCrv, "{0}_ikSpl_CRV".format(name))    
    return(splHandle, splEffector, splCrv)


def create_joint_chain(name, startVec, endVec, numJnts):
    cmds.select(cl=True)
    jntList = rig.create_joint_chain(startVec, endVec, numJnts, "{0}_bind".format(name))
    return(jntList) 


def create_control_joints(startVec, endVec, name):
    # make joints at start and end pos
    ctrlJntList = []
    midVec = rig.linear_interpolate_vector(startVec, endVec, .5)
    vecList = [startVec,midVec, endVec]
    nameList  = ["{0}_Base_JNT".format(name), "{0}_Mid_JNT".format(name), "{0}_Top_JNT".format(name)] 
    for x in range(3):
        cmds.select(cl=True)
        jnt = cmds.joint(name=nameList[x], position=vecList[x])
        ctrlJntList.append(jnt)
    return(ctrlJntList)


def create_tangent_joints(startVec, endVec, name, midVal):
    tanJntList = []
    # get values for linear interp
    tan1Perc = midVal*0.5
    tan2Perc = 1-((1-midVal)*0.5)
    cmds.select(cl=True)
    tanBase = cmds.joint(name="{0}_Base_tangent_JNT".format(name), position=rig.linear_interpolate_vector(startVec, endVec, tan1Perc))
    cmds.select(cl=True)
    tanTop = cmds.joint(name="{0}_Top_tangent_JNT".format(name), position=rig.linear_interpolate_vector(startVec, endVec, tan2Perc))
    cmds.select(cl=True)
    return([tanBase, tanTop])


def create_controls(jntList, name, axis, ctrlType, color):
    ctrls = []
    for jnt in jntList:
        name = jnt.rpartition("_")[0]+"_CTRL"
        ctrl = rig.create_control(name, ctrlType, axis, color)
        grp = rig.group_freeze(ctrl)
        rig.snap_to(jnt, grp)
        ctrls.append([ctrl, grp])
    return(ctrls)
        

def constrain_joints(ctrlList, JntList):
    constraintList = []
    for x in range(len(ctrlList)):
        pc = cmds.parentConstraint(ctrlList[x][0], JntList[x])
        constraintList.append(pc)

    return(constraintList)


def setup_scaling(name, splCrv, jntList, topCtrl):
    measureCrv = cmds.duplicate(splCrv,name="{0}_measure_CRV".format(name))[0]
    splPoc = cmds.arclen(splCrv, ch=True)
    msrPoc = cmds.arclen(measureCrv, ch=True)
    ratioMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_ratio_mult".format(name))
    cmds.setAttr("{0}.operation".format(ratioMult), 2)
    cmds.connectAttr("{0}.arcLength".format(splPoc), "{0}.input1.input1X".format(ratioMult))
    cmds.connectAttr("{0}.arcLength".format(msrPoc), "{0}.input2.input2X".format(ratioMult))
# add in turnoff switch for scale
    scaleDefaultMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_envelope_mult".format(name))
    cmds.setAttr("{0}.input1X".format(scaleDefaultMult), 1.0)
    envelopeBlend = cmds.shadingNode("blendColors", asUtility=True, name="{0}_scaleBlClr".format(name))
    cmds.connectAttr("{0}.auto_stretch".format(topCtrl), "{0}.blender".format(envelopeBlend))
    cmds.connectAttr("{0}.outputX".format(ratioMult), "{0}.color1.color1R".format(envelopeBlend))
    cmds.connectAttr("{0}.outputX".format(scaleDefaultMult), "{0}.color2.color2R".format(envelopeBlend))

    for jnt in jntList[:-1]:
        cmds.connectAttr("{0}.output.outputR".format(envelopeBlend), "{0}.sx".format(jnt))
    return(measureCrv)


def setup_spline_advanced_twist(handle, startObj, endObj, fwdAxis=0, upAxis=3):
    """
    ARGS:
        handle(str): the ikspline handle
        startObj(str): the xform of the start obj
        endObj(str): the xform of the end obj
        fwdAxis(int): 0 is x, 1 is -x, etc
        upAxis(int): 0, 1, 2 = +y, -y, closest y, (then z then x)
    """
    cmds.setAttr("{0}.dWorldUpType".format(handle), 4) # sets twist to objRotUpStartEnd
    cmds.setAttr("{0}.dTwistControlEnable".format(handle), 1)
    cmds.setAttr("{0}.dForwardAxis".format(handle), fwdAxis)
    cmds.setAttr("{0}.dWorldUpAxis".format(handle), upAxis)

    cmds.setAttr("{0}.dWorldUpVector".format(handle), 0, 0, 1)
    cmds.setAttr("{0}.dWorldUpVectorEnd".format(handle), 0, 0, 1)

    cmds.connectAttr("{0}.worldMatrix[0]".format(startObj), "{0}.dWorldUpMatrix".format(handle))
    cmds.connectAttr("{0}.worldMatrix[0]".format(endObj), "{0}.dWorldUpMatrixEnd".format(handle))

    cmds.setAttr("{0}.dTwistValueType".format(handle), 0) # sets to total


def bind_skin(jntList, objList):
    skin = cmds.skinCluster(jntList, objList, maximumInfluences=5, smoothWeights=0.5, obeyMaxInfluences=False, toSelectedBones=True, normalizeWeights=1)


def connect_attributes(name, ctrl, tanlist, oc, ptc):
    #create default value of tangents mults, then blend between that and zero
    baseDefaultMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_baseDefaultTrans_mult".format(name))
    baseZeroMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_baseZeroTrans_mult".format(name))
    bt = cmds.getAttr("{0}.t".format(tanlist[0][1]))[0]
    cmds.setAttr("{0}.input1".format(baseDefaultMult), bt[0], bt[1], bt[2])
    baseBlend = cmds.shadingNode("blendColors", asUtility=True, name="{0}_base_bldClr".format(name))
    cmds.connectAttr("{0}.output".format(baseZeroMult), "{0}.color2".format(baseBlend))
    cmds.connectAttr("{0}.output".format(baseDefaultMult), "{0}.color1".format(baseBlend))
    topDefaultMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_topDefaultTrans_mult".format(name))
    topZeroMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_topZeroTrans_mult".format(name))
    tt = cmds.getAttr("{0}.t".format(tanlist[1][1]))[0]
    cmds.setAttr("{0}.input1".format(topDefaultMult), tt[0], tt[1], tt[2])
    topBlend = cmds.shadingNode("blendColors", asUtility=True, name="{0}_top_bldClr".format(name))
    cmds.connectAttr("{0}.output".format(topZeroMult), "{0}.color2".format(topBlend))
    cmds.connectAttr("{0}.output".format(topDefaultMult), "{0}.color1".format(topBlend))
    cmds.connectAttr("{0}.tangents".format(ctrl), "{0}.blender".format(baseBlend))
    cmds.connectAttr("{0}.tangents".format(ctrl), "{0}.blender".format(topBlend))
    
    cmds.connectAttr("{0}.output".format(baseBlend), "{0}.t".format(tanlist[0][1]))
    cmds.connectAttr("{0}.output".format(topBlend), "{0}.t".format(tanlist[1][1]))

    #connect visibility
    cmds.connectAttr("{0}.tangents".format(ctrl), "{0}.v".format(tanlist[0][0]))
    cmds.connectAttr("{0}.tangents".format(ctrl), "{0}.v".format(tanlist[1][0]))

#----------------how to elegantly turn off constraints by blending?
#----------------only need one control rotate doesn't do much
    ptcAttr = cmds.listConnections(ptc, p=True, s=True, type="constraint")[:2]
    ocAttr =  cmds.listConnections(oc, p=True, s=True, type="constraint")[:2]
    for x in range(2):
        cmds.connectAttr("{0}.midFollowsRotation".format(ctrl), ocAttr[x])
        cmds.connectAttr("{0}.midFollowsPosition".format(ctrl), ptcAttr[x])


def clean_up(*args):
    # hide vis of ikSPlne
    # group things properly
    pass

def ikSpine(): 
    # kwargs = {
    #     "baseObj":"a",
    #     "endObj":"b",
    #     "numJnts": 20,
    #     "name": "upArm"
    # }
    ikSpine_UI()