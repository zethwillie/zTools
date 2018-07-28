import maya.cmds as cmds

import zTools.rig.zbw_rig as rig
reload(rig)
# get how many ctrls we want, then make cureve have that many cvs
# refactor this out to functions - outputs for api style


#----------------UI

def create_ikspline_rig(topJnt, lowJnt, numJnts, name=None):

    if not name:
        name=topJnt

    name = name + "_spline"

    topPos = cmds.xform(topJnt, ws=True, q=True, rp=True)
    topRot = cmds.xform(topJnt, ws=True, q=True, ro=True)
    lowPos = cmds.xform(lowJnt, ws=True, q=True, rp=True)

#---------------- do this with a measure
    dist = cmds.getAttr("{0}.tx".format(lowJnt))

    jntList = []
    factor = dist/float(numJnts-1)

#----------------option to do with joints or with other transforms? or just pts?
    for i in range(numJnts):
        jnt = cmds.duplicate(topJnt, po=True, name="{0}_ik_{1}".format(name, i))[0]
        if i !=  0:
            cmds.parent(jnt, jntList[0])
            cmds.setAttr("{0}.tx".format(jnt), i*factor)
        jntList.append(jnt)
        
    for x in range(len(jntList)):
        if x > 1:
            cmds.parent(jntList[x], jntList[x-1])

#----------------orient jnts to make sure it's in x 

    splHandle, splEffector, splCrv = cmds.ikHandle(startJoint=jntList[0], ee=jntList[-1], sol="ikSplineSolver", numSpans=1, rootTwistMode=False, parentCurve=False, name="{0}_IK".format(name))
    splCrv = cmds.rename(splCrv, "{0}_splCrv".format(name))

    bindJnts = []
    bindGrps = []
    bindCtrls = []
    offsetGrps = []
    
    # this into a loop for however many ctrls we need? 
    ctrlNames = ["base", "mid", "end"]
    for cName in ctrlNames:
        ctrl = rig.createControl("{0}_{1}_CTRL".format(cName, name), "circle", color="red")
        grp  = rig.groupFreeze(ctrl)
        cmds.select(cl=True)
        jnt = cmds.joint(name="{0}_{1}_JNT".format(cName, name))
        cmds.parent(jnt, ctrl)
        offsetGrp = rig.groupFreeze(grp, suffix="offset")
        topGrp = rig.groupFreeze(offsetGrp)
        topGrp = cmds.rename(topGrp, "{0}_{1}_ctrl_GRP".format(cName, name))
        bindJnts.append(jnt)
        bindGrps.append(topGrp)
        bindCtrls.append(ctrl)
        offsetGrps.append(offsetGrp)

    percent = 1.0/(len(ctrlNames)-1)
    for i in range(len(ctrlNames)):
        # snap to cvs? 
        rig.snapTo(topJnt, bindGrps[i])
        pos = rig.linear_interpolate_vector(topPos, lowPos, i*percent)
        cmds.xform(bindGrps[i], ws=True, t=pos)

    pc = cmds.pointConstraint([bindCtrls[0], bindCtrls[2]], offsetGrps[1], mo=True)[0]
    oc = cmds.orientConstraint([bindCtrls[0], bindCtrls[2]], offsetGrps[1], mo=True)[0]

    measureCrv = cmds.duplicate(splCrv,name="{0}_measure_CRV".format(name))[0]
    splPoc = cmds.arclen(splCrv, ch=True)
    msrPoc = cmds.arclen(measureCrv, ch=True)
    ratioMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_ratio_mult".format(name))
    cmds.setAttr("{0}.operation".format(ratioMult), 2)
    cmds.connectAttr("{0}.arcLength".format(splPoc), "{0}.input1.input1X".format(ratioMult))
    cmds.connectAttr("{0}.arcLength".format(msrPoc), "{0}.input2.input2X".format(ratioMult))

    for jnt in jntList[:-1]:
        cmds.connectAttr("{0}.output.outputX".format(ratioMult), "{0}.sx".format(jnt))

    bind_skin(bindJnts, splCrv)

#---------------- deal with end jnt flipping (add a joint/s at the postion of the "B" jnt)
#---------------- weight the cvs of the crv to those jnts

    setup_spline_advanced_twist(splHandle, bindCtrls[0], bindCtrls[2], 0, 0)

#---------------- option to turn off stretching
#---------------- squash and stretch on a ramp which tells where the effect takes place along the curve
#---------------- attrs to lengthen and shorten the curve

    cmds.addAttr(bindCtrls[1], ln="startTwist", k=True, dv=0, at="float")
    cmds.addAttr(bindCtrls[1], ln="endTwist", k=True, dv=0, at="float")
    cmds.connectAttr("{0}.startTwist".format(bindCtrls[1]), "{0}.dTwistStart".format(splHandle))
    cmds.connectAttr("{0}.endTwist".format(bindCtrls[1]), "{0}.dTwistEnd".format(splHandle))
    cmds.addAttr(bindCtrls[1], ln="followEnds", k=True, dv=0, at="float", min=0, max=1)
    cmds.connectAttr("{0}.followEnds".format(bindCtrls[1]), "{0}.{1}W0".format(pc, bindCtrls[0]))
    cmds.connectAttr("{0}.followEnds".format(bindCtrls[1]), "{0}.{1}W1".format(pc, bindCtrls[2]))

    finalCtrlGrp = cmds.group(em=True, name="{0}_driverCtrl_GRP".format(name))
    cmds.parent(bindGrps, finalCtrlGrp)
    xformGrp = cmds.group(em=True, name="{0}_transform_GRP".format(name))
    cmds.parent([finalCtrlGrp, measureCrv, jntList[0]], xformGrp)
    noXformGrp = cmds.group(em=True, name="{0}_noTransform_GRP".format(name))
    cmds.parent([splCrv, splHandle], noXformGrp)

    hide = [measureCrv, splCrv, splHandle]
    for obj in hide:
        cmds.setAttr("{0}.v".format(obj), 0)

def setup_spline_advanced_twist(handle, startObj, endObj, fwdAxis=0, upAxis=0):
    """
    ARGS:
        handle(str): the ikspline handle
        startObj(str): the transform of the start obj
        endObj(str): the xform of the end obj
        fwdAxis(int): 0 is x, 1 is -x, etc
        upAxis(int): 0, 1, 2 = +y, -y, closest y, (then z then x)
    """
    cmds.setAttr("{0}.dWorldUpType".format(handle), 4) # sets twist to objRotUp
    cmds.setAttr("{0}.dTwistControlEnable".format(handle), 1)
    cmds.setAttr("{0}.dForwardAxis".format(handle), 0)
    cmds.setAttr("{0}.dWorldUpAxis".format(handle), 0)

    cmds.setAttr("{0}.dWorldUpVector".format(handle), 0, 1, 0)
    cmds.setAttr("{0}.dWorldUpVectorEnd".format(handle), 0, 1, 0)

    cmds.connectAttr("{0}.worldMatrix[0]".format(startObj), "{0}.dWorldUpMatrix".format(handle))
    cmds.connectAttr("{0}.worldMatrix[0]".format(endObj), "{0}.dWorldUpMatrixEnd".format(handle))

    cmds.setAttr("{0}.dTwistValueType".format(handle), 1) # sets to start/end


def bind_skin(jntList, objList):
        skin = cmds.skinCluster(jntList, objList, maximumInfluences=5, smoothWeights=0.5, obeyMaxInfluences=False, toSelectedBones=True, normalizeWeights=1)


def splineRig(): 
    kwargs = {
        "topJnt":"a",
        "lowJnt":"b", 
        "numJnts": 20, 
        "name": "upArm"
    }
    create_ikspline_rig(**kwargs)