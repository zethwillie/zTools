import maya.cmds as cmds
import zTools.rig.zbw_rig as rig
reload(rig)

# OOP version, clean up
# UI can just feed info into the class for now
# now we can do things like axis, etc

class IKSpine(object):
    def __init__(self, basePos=[0, 0, 0], topPos=[0, 10, 0], numJnts=20, name="ikSpine", midVal=0.5):
        # set init values
        self.basePos = basePos
        self.topPos = topPos
        self.numJnt = numJnts
        self.name = name
        self.numJnts = numJnts
        self.midVal = midVal

        self.create_ikspine_rig()

    def create_ikspine_rig(self):
        #create joints
        self.jntList = self.create_joint_chain()
        #create ik spline
        self.splHandle, self.splEffector, self.splCrv = self.create_ik_spline()
        #create control joints
        self.ctrlJnts = self.create_control_joints()
        #create tangent joints
        self.tanJnts = self.create_tangent_joints()
        # create controls for control joints
        self.ctrlJntCtrls = self.create_controls(self.ctrlJnts, "CTRL", "y", "box", "yellow")
        self.create_attributes(self.ctrlJntCtrls[2][0])
        # create controls for tangents
        self.tanJntCtrls = self.create_controls(self.tanJnts, "CTRL", "y", "star", "darkPurple")
        self.attach_ctrls()
         # bind ctrl joints to curve
        self.bind_skin(self.ctrlJnts, self.splCrv)
        # setup twist on ik spline
        self.setup_spline_advanced_twist()
        self.measureCrv = self.setup_scaling()
        self.connect_attributes()
        self.clean_up()
#---------------- deal with end jnt flipping (add a joint/s at the postion of the "B" jnt)
#---------------- squash and stretch on a ramp which tells where the effect takes place along the curve (ie. move joints up and down curve?)


    def create_attributes(self, ctrl):
        cmds.addAttr(ctrl, ln="auto_stretch", at="double", min=0, max=1, k=True, dv=0)
        cmds.addAttr(ctrl, ln="tangents", at="double", min=0, max=1, k=True, dv=1)
        cmds.addAttr(ctrl, ln="midFollowsPosition", at="double", min=0, max=1, k=True, dv=1)
        cmds.addAttr(ctrl, ln="midFollowsRotation", at="double", min=0, max=1, k=True, dv=1)


    def attach_ctrls(self):
       #parent tangents in
        cmds.parent(self.tanJntCtrls[0][1], self.ctrlJntCtrls[0][0]) 
        cmds.parent(self.tanJntCtrls[1][1], self.ctrlJntCtrls[2][0]) 
        # attach controls to ctrl joints
        self.ctrlPCs = self.constrain_joints(self.ctrlJntCtrls, self.ctrlJnts)
        self.tanPCs = self.constrain_joints(self.tanJntCtrls, self.tanJnts)
        self.midPtC = cmds.pointConstraint(self.tanJnts, self.ctrlJntCtrls[1][1])
        self.midOC = cmds.orientConstraint(self.tanJnts, self.ctrlJntCtrls[1][1])


    def create_ik_spline(self):
    #----------------check setting here, crv should have 3 or 4 spans?  Root twist mode   
        splHandle, splEffector, splCrv = cmds.ikHandle(startJoint=self.jntList[0], ee=self.jntList[-1], sol="ikSplineSolver", numSpans=2, rootTwistMode=True, parentCurve=False, name="{0}_IK".format(self.name))
        splCrv = cmds.rename(splCrv, "{0}_ikSpl_CRV".format(self.name))    
        return(splHandle, splEffector, splCrv)


    def create_joint_chain(self):
        cmds.select(cl=True)
        jntList = rig.create_joint_chain(self.basePos, self.topPos, self.numJnts, "{0}_bind".format(self.name))
        return(jntList) 


    def create_control_joints(self):
        # make joints at start and end pos
        ctrlJntList = []
        midVec = rig.linear_interpolate_vector(self.basePos, self.topPos, self.midVal)
        vecList = [self.basePos,midVec, self.topPos]
        nameList  = ["{0}_Base_JNT".format(self.name), "{0}_Mid_JNT".format(self.name), "{0}_Top_JNT".format(self.name)] 
        for x in range(3):
            cmds.select(cl=True)
            jnt = cmds.joint(name=nameList[x], position=vecList[x])
            ctrlJntList.append(jnt)
        return(ctrlJntList)


    def create_tangent_joints(self):
        tanJntList = []
        # get values for linear interp
        tan1Perc = self.midVal*0.5
        tan2Perc = 1-((1-self.midVal)*0.5)
        cmds.select(cl=True)
        tanBase = cmds.joint(name="{0}_Base_tangent_JNT".format(self.name), position=rig.linear_interpolate_vector(self.basePos, self.topPos, tan1Perc))
        cmds.select(cl=True)
        tanTop = cmds.joint(name="{0}_Top_tangent_JNT".format(self.name), position=rig.linear_interpolate_vector(self.basePos, self.topPos, tan2Perc))
        cmds.select(cl=True)
        return([tanBase, tanTop])


    def create_controls(self, jntList, name, axis, ctrlType, color):
        ctrls = []
        for jnt in jntList:
            name = jnt.rpartition("_")[0]+"_CTRL"
            ctrl = rig.create_control(name, ctrlType, axis, color)
            grp = rig.group_freeze(ctrl)
            rig.snap_to(jnt, grp)
            ctrls.append([ctrl, grp])
        return(ctrls)
            

    def constrain_joints(self, ctrlList, JntList):
        constraintList = []
        for x in range(len(ctrlList)):
            pc = cmds.parentConstraint(ctrlList[x][0], JntList[x])
            constraintList.append(pc)

        return(constraintList)


    def setup_scaling(self):
        measureCrv = cmds.duplicate(self.splCrv,name="{0}_measure_CRV".format(self.name))[0]
        splPoc = cmds.arclen(self.splCrv, ch=True)
        msrPoc = cmds.arclen(measureCrv, ch=True)
        ratioMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_ratio_mult".format(self.name))
        cmds.setAttr("{0}.operation".format(ratioMult), 2)
        cmds.connectAttr("{0}.arcLength".format(splPoc), "{0}.input1.input1X".format(ratioMult))
        cmds.connectAttr("{0}.arcLength".format(msrPoc), "{0}.input2.input2X".format(ratioMult))
        scaleDefaultMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_envelope_mult".format(self.name))
        cmds.setAttr("{0}.input1X".format(scaleDefaultMult), 1.0)
        envelopeBlend = cmds.shadingNode("blendColors", asUtility=True, name="{0}_scaleBlClr".format(self.name))
        cmds.connectAttr("{0}.auto_stretch".format(self.ctrlJntCtrls[2][0]), "{0}.blender".format(envelopeBlend))
        cmds.connectAttr("{0}.outputX".format(ratioMult), "{0}.color1.color1R".format(envelopeBlend))
        cmds.connectAttr("{0}.outputX".format(scaleDefaultMult), "{0}.color2.color2R".format(envelopeBlend))

        for jnt in self.jntList[:-1]:
            cmds.connectAttr("{0}.output.outputR".format(envelopeBlend), "{0}.sx".format(jnt))
        return(measureCrv)


    def setup_spline_advanced_twist(self):
        cmds.setAttr("{0}.dWorldUpType".format(self.splHandle), 4) # sets twist to objRotUpStartEnd
        cmds.setAttr("{0}.dTwistControlEnable".format(self.splHandle), 1)
        cmds.setAttr("{0}.dForwardAxis".format(self.splHandle), 0)
        cmds.setAttr("{0}.dWorldUpAxis".format(self.splHandle), 3)

        cmds.setAttr("{0}.dWorldUpVector".format(self.splHandle), 0, 0, 1)
        cmds.setAttr("{0}.dWorldUpVectorEnd".format(self.splHandle), 0, 0, 1)

        cmds.connectAttr("{0}.worldMatrix[0]".format(self.ctrlJntCtrls[0][0]), "{0}.dWorldUpMatrix".format(self.splHandle))
        cmds.connectAttr("{0}.worldMatrix[0]".format(self.ctrlJntCtrls[2][0]), "{0}.dWorldUpMatrixEnd".format(self.splHandle))

        cmds.setAttr("{0}.dTwistValueType".format(self.splHandle), 0) # sets to total


    def bind_skin(self, jntList, objList):
        skin = cmds.skinCluster(jntList, objList, maximumInfluences=5, smoothWeights=0.5, obeyMaxInfluences=False, toSelectedBones=True, normalizeWeights=1)


    def connect_attributes(self):
        name = self.name
        ctrl = self.ctrlJntCtrls[2][0]
        tanlist = self.tanJntCtrls
        oc = self.midOC
        ptc = self.midPtC
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


    def clean_up(self):
        # hide spline ikhandle, measure curve, ikCrv 
        toHide = [self.splHandle, self.measureCrv, self.splCrv]
        for obj in toHide:
            cmds.setAttr("{0}.v".format(obj), 0)
        # create noTransform group (turn off inh xforms)
        self.noTransformGrp = cmds.group(em=True, name="{0}_noTransform_GRP".format(self.name))
        cmds.setAttr("{0}.inheritsTransform".format(self.noTransformGrp), 0)
        cmds.parent([self.splHandle, self.splCrv], self.noTransformGrp)
        self.transformGrp = cmds.group(em=True, name="{0}_transform_GRP".format(self.name))
        cmds.parent([self.jntList[0], self.tanJnts[0], self.tanJnts[1], self.ctrlJntCtrls[0][1], self.ctrlJntCtrls[1][1], self.ctrlJntCtrls[2][1], self.ctrlJnts[0], self.ctrlJnts[1], self.ctrlJnts[2], self.measureCrv], self.transformGrp)