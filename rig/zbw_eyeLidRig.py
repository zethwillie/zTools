import maya.cmds as cmds
import maya.OpenMaya as om
import zTools.rig.zbw_rig as rig
reload(rig)


class EyelidRigUI(object):
    def __init__(self):
    # in UI:
        # get center of eyeball obj? 
        # create curve from edges
        # test whether they're facing same dir (compare first eps?)
        # pause to orient objects?
        # way to duplicate curves across x and create the rig there. . .
        # do we need to do this in one pass here?
        pass
        

class EyelidRigBuild(object):

    def __init__(self, name="eye", cnt=None, up=None, num=5, topCrv=None, botCrv=None, blend=1):
        """
        blend(int): 1 = grp things for blend shaping into rig, 0 = grp things for attaching into rig
        """
        if not (cnt and up):
            cmds.warning("You haven't provided a center and up object!")
            return()
        if not (topCrv and botCrv):
            cmds.warning("You haven't provided up and down curves!")
            return()

        self.name = name
        self.center = cnt
        self.up = up
        self.numCtrl = num
        self.topHiresCrv = cmds.rename(topCrv, "{0}_top_hi_CRV".format(name))
        self.botHiresCrv = cmds.rename(botCrv, "{0}_bot_hi_CRV".format(name))
        self.blend = blend
        self.centerPos = cmds.xform(self.center, q=True, ws=True, rp=True)

        self.sides = ["top", "bot"]
        self.blinkCrvs = []
        self.blinkCrvGrp = cmds.group(empty=True, n="{0}_blink_crv_GRP".format(self.name))
        self.center_pivot([self.blinkCrvGrp])

        self.eyeRig = {"top":{}, "bot":{}}
        for side in self.sides:
            self.eyeRig[side]["crvList"] = []
            self.eyeRig[side]["crvGrp"] = cmds.group(empty=True, n="{0}_{1}_CRV_GRP".format(self.name, side))
            self.eyeRig[side]["locList"] = []
            self.eyeRig[side]["locGrp"] = cmds.group(empty=True, n="{0}_{1}_AIMLOC_GRP".format(self.name, side))
            self.eyeRig[side]["bindJntList"] = []
            self.eyeRig[side]["bindJntGrp"] = cmds.group(empty=True, n="{0}_{1}_BNDJNT_GRP".format(self.name, side))
            self.eyeRig[side]["bindCtrlList"] = []
            self.eyeRig[side]["bindCtrlGrp"] = cmds.group(empty=True, n="{0}_{1}_FINECTRL_GRP".format(self.name, side))
            self.eyeRig[side]["wires"] = []
            self.eyeRig[side]["wireBases"] = []
            self.eyeRig[side]["ctrlJntList"] = []
            self.eyeRig[side]["ctrlJntGrps"] = cmds.group(empty=True, n="{0}_{1}_ctrlJnt_GRP".format(self.name, side))
            self.eyeRig[side]["ctrlList"] = []
            self.eyeRig[side]["ctrlGrpList"] = []
            self.eyeRig[side]["ctrlsGrp"] = cmds.group(empty=True, n="{0}_{1}_ctrls_GRP".format(self.name, side))
            self.eyeRig[side]["proxyList"] = []
            self.eyeRig[side]["proxyGrpList"] = []
            self.eyeRig[side]["proxyGrp"] = cmds.group(empty=True, n="{0}_{1}_proxies_GRP".format(self.name, side))

            grps = [self.eyeRig[side]["crvGrp"], self.eyeRig[side]["bindJntGrp"], self.eyeRig[side]["locGrp"], self.eyeRig[side]["bindCtrlGrp"], self.eyeRig[side]["ctrlJntGrps"], self.eyeRig[side]["ctrlsGrp"], self.eyeRig[side]["proxyGrp"]]
            self.center_pivot(grps)

            if side == "top":
                cmds.parent(self.topHiresCrv, self.eyeRig[side]["crvGrp"])
            if side == "bot":
                cmds.parent(self.botHiresCrv, self.eyeRig[side]["crvGrp"])

        self.eyeRig["top"]["crvList"].append(self.topHiresCrv)
        self.eyeRig["bot"]["crvList"].append(self.botHiresCrv)
        
        self.create_rig()


    def create_rig(self):
        for side in self.eyeRig.keys():
            # hiresCrv = self.eyeRig[side]["crvList"][0]
            self.create_locs_joints_at_curve(side)
            self.create_control_joints(side)
            self.create_control_wire_deformer(side)
            self.bind_control_curve(side)
            self.create_and_connect_ctrls(side)
            # can we orient off of eyeball? Does that make sense?
        self.smart_blink_setup()
        self.clean_up_rig()


    def center_pivot(self, clist):
        for obj in clist:
            cmds.xform(obj, ws=True, rp=self.centerPos)
            cmds.xform(obj, ws=True, sp=self.centerPos)


    def create_locs_joints_at_curve(self, side=None):

        crv = self.eyeRig[side]["crvList"][0]
        eps = cmds.ls("{0}.ep[*]".format(crv), fl=True)

        for x in range(len(eps)):
            loc = cmds.spaceLocator(n="{0}_{1}_{2}_LOC".format(self.name, side, x))[0]
            self.eyeRig[side]["locList"].append(loc)
            cmds.connectAttr(eps[x], "{0}.t".format(loc))
            cmds.setAttr("{0}.localScale".format(loc), 0.1, 0.1, 0.1)
            locPos = cmds.xform(loc, q=True, ws=True, rp=True)
            cmds.select(cl=True)
            baseJnt = cmds.joint(n="baseJnt_{0}{1}".format(crv[:-4], x), position=self.centerPos)
            endJnt = cmds.joint(n="endJnt_{0}{1}".format(crv[:-4], x), position=locPos)
            tmpEndJnt = self.extend_joint_chain(endJnt)
            cmds.select(cl=True)
            cmds.joint(baseJnt, e=True, oj="xyz", sao="yup", ch=True)
            cmds.delete(tmpEndJnt)
            self.eyeRig[side]["bindJntList"].append(baseJnt)

            cmds.parent(baseJnt, self.eyeRig[side]["bindJntGrp"])
            cmds.parent(loc, self.eyeRig[side]["locGrp"])

            ac = cmds.aimConstraint(loc, baseJnt, mo=False, wuo=self.up, wut="object", aim=(1,0,0), u=(0,1,0))

        # put controls on indiv joints for fine ctrl, create proxy for these? we have groups for these.

    def extend_joint_chain(self, endObj, baseObj=None):
        # get vector from par to endJnt
        if not baseObj:
            par = cmds.listRelatives(endObj, p=True)[0]
            pPos = cmds.xform(par, q=True, ws=True, rp=True)
        else:
            pPos = cmds.xform(baseObj, q=True, ws=True, rp=True)
        jPos = cmds.xform(endObj, q=True, ws=True, rp=True)
        parPos = om.MVector(pPos[0], pPos[1], pPos[2])
        jntPos = om.MVector(jPos[0], jPos[1], jPos[2])

        vec = jntPos - parPos
        newPos = jntPos + (vec*.25)
        cmds.select(cl=True)
        tmpEndJoint = cmds.joint(name="{0}_temp".format(endObj), p=newPos)
        cmds.parent(tmpEndJoint, endObj)
        return(tmpEndJoint)


    def create_control_joints(self, side=None):
        crv = self.eyeRig[side]["crvList"][0]
        ctrlCrvName = crv.replace("_hi_", "_ctrl_")
        ctrlCrv = rig.rebuild_curve(curve=crv, num=self.numCtrl-1, name=ctrlCrvName, keep=True, ch=False)
        self.eyeRig[side]["crvList"].append(ctrlCrv)

        ctrlEps = cmds.ls("{0}.ep[*]".format(ctrlCrv), fl=True)

        # create joints
        for x in range(0, len(ctrlEps)):
            pos = cmds.getAttr(ctrlEps[x])[0]
            cmds.select(cl=True)
            jnt = cmds.joint(n="{0}_Jnt{1}".format(ctrlCrv, x), position=pos)
#---------------- orient this to eyelid?
            tmpEndJnt = self.extend_joint_chain(jnt, self.center)
            cmds.joint(jnt, e=True, oj="xyz", sao="yup", ch=True)
            cmds.delete(tmpEndJnt)
            jntGrp = rig.group_freeze(jnt)
            cmds.parent(jntGrp, self.eyeRig[side]["ctrlJntGrps"])
            self.eyeRig[side]["ctrlJntList"].append(jnt)


    def create_control_wire_deformer(self, side):
        wireNode = cmds.wire(self.eyeRig[side]["crvList"][0], envelope=1, groupWithBase=False, crossingEffect=0, localInfluence=0, wire=self.eyeRig[side]["crvList"][1], name="{0}_{1}_ctrl_WIRE".format(self.name, side))[0]
        wireBase = self.get_base_wire(wireNode)
        self.eyeRig[side]["wireBases"].append(wireBase)
        self.eyeRig[side]["wires"].append(wireNode)

        cmds.parent(self.eyeRig[side]["crvList"][1], self.eyeRig[side]["crvGrp"])
        cmds.parent(wireBase, self.eyeRig[side]["crvGrp"])


    def bind_control_curve(self, side):
        skinCluster = self.bind_crv_to_joints(self.eyeRig[side]["crvList"][1], self.eyeRig[side]["ctrlJntList"])


    def create_and_connect_ctrls(self, side):
        # create ctrls
        sideGrps = self.create_ctrls_for_joints(side)
        sideProxies = self.connect_ctrl_via_proxies(side)


    def bind_crv_to_joints(self, crv, jntList):
        skinCluster = cmds.skinCluster(jntList, crv, maximumInfluences=3, dropoffRate=4, skinMethod=0, normalizeWeights=2)
        return(skinCluster)

    def get_base_wire(self, wireDef):
        shp = cmds.listConnections(wireDef+".baseWire[0]", p=True, s=True)[0].split(".")[0]
        basewire = cmds.listRelatives(shp, p=True)[0]
        return(basewire)


    def create_ctrls_for_joints(self, side):
#----------------scale attr from ui to scale the ctrls
        for jnt in self.eyeRig[side]["ctrlJntList"]:
            ctrlName = "{0}_{1}_{2}_CTRL".format(self.name, side, self.eyeRig[side]["ctrlJntList"].index(jnt))
            ctrl = rig.create_control(name=ctrlName, type="circle", axis="x", color="blue")
            grp = rig.group_freeze(ctrl)
            self.eyeRig[side]["ctrlList"].append(ctrl)
            self.eyeRig[side]["ctrlGrpList"].append(grp)
            rig.snap_to(jnt, grp)
            cmds.parent(grp, self.eyeRig[side]["ctrlsGrp"])


    def connect_ctrl_via_proxies(self, side):
        for grp in self.eyeRig[side]["ctrlGrpList"]:
            index = self.eyeRig[side]["ctrlGrpList"].index(grp)
            ctrl = self.eyeRig[side]["ctrlList"][index]
            ctrlProxy, grpProxy = rig.create_space_buffer_grps(ctrl)
            cmds.parent(grpProxy, self.eyeRig[side]["proxyGrp"])
            self.eyeRig[side]["proxyList"].append(ctrlProxy)
            self.eyeRig[side]["proxyGrpList"].append(grpProxy)
            # connect with joint
            rig.connect_transforms(ctrlProxy, self.eyeRig[side]["ctrlJntList"][index])

            # Do we need to add another layer of this? Don't think so. . . 

    def smart_blink_setup(self):
        closeCrv = cmds.duplicate(self.eyeRig["top"]["crvList"][1], name="{0}_blinkLowres".format(self.name))[0]
        cmds.parent(closeCrv, self.blinkCrvGrp)
        self.blinkCrvs.append(closeCrv)
        
        midBS = cmds.blendShape(self.eyeRig["top"]["crvList"][1], self.eyeRig["bot"]["crvList"][1], closeCrv)[0]
        midTopAttr = "{0}.{1}".format(midBS, self.eyeRig["top"]["crvList"][1])
        midBotAttr = "{0}.{1}".format(midBS, self.eyeRig["bot"]["crvList"][1])
        # dupe bot hirez crvs and create wires
        cmds.setAttr(midTopAttr, 0)
        cmds.setAttr(midBotAttr, 1)
        # rename base wire crv    
        botBlinkTgt = cmds.duplicate(self.eyeRig["bot"]["crvList"][0], name="{0}_bot_blinkTarget".format(self.name))[0]
        cmds.parent(botBlinkTgt, self.blinkCrvGrp)

        topBlinkTgt = cmds.duplicate(self.eyeRig["top"]["crvList"][0], name="{0}_top_blinkTarget".format(self.name))[0]
        cmds.parent(topBlinkTgt, self.blinkCrvGrp)

        botBlinkWire = cmds.wire(botBlinkTgt, envelope=1, groupWithBase=False, crossingEffect=0, localInfluence=0, w=closeCrv, name = "{0}_botBlink_WIRE".format(self.name))[0]
        # rename base wire crv    
        wireBotBaseCrv = self.get_base_wire(botBlinkWire)
        self.eyeRig["bot"]["wireBases"].append(wireBotBaseCrv)
        cmds.setAttr("{0}.scale[0]".format(botBlinkWire), 0)

        cmds.setAttr(midTopAttr, 1)
        cmds.setAttr(midBotAttr, 0)
        topBlinkWire = cmds.wire(topBlinkTgt, envelope=1, groupWithBase=False, crossingEffect=0, localInfluence=0, w=closeCrv, name = "{0}_topBlink_WIRE".format(self.name))[0]
        wireTopBaseCrv = self.get_base_wire(topBlinkWire)
        self.eyeRig["top"]["wireBases"].append(wireTopBaseCrv)
        cmds.setAttr("{0}.scale[0]".format(topBlinkWire), 0)

        #cmds.parent(self.eyeRig["top"]["crvList"][0], self.eyeRig["top"]["crvGrp"])
        # blend shape hires curves to top, bot blink curves
        topBlinkBlend = cmds.blendShape(topBlinkTgt, self.eyeRig["top"]["crvList"][0], name="{0}_top_blink_BS".format(self.name))[0]
        topBlendAttr = "{0}.{1}".format(topBlinkBlend, topBlinkTgt)

        botBlinkBlend = cmds.blendShape(botBlinkTgt, self.eyeRig["bot"]["crvList"][0], name="{0}_bot_blink_BS".format(self.name))[0]
        botBlendAttr = "{0}.{1}".format(botBlinkBlend, botBlinkTgt)
        
        # put attrs on mid ctrls
        topCtrl = self.eyeRig["top"]["ctrlList"][2]
        botCtrl = self.eyeRig["bot"]["ctrlList"][2]

        cmds.addAttr(topCtrl, ln="__xtraAttrs__", at="enum", en="-----", k=True)
        cmds.addAttr(botCtrl, ln="__xtraAttrs__", at="enum", en="-----", k=True)
        cmds.setAttr("{0}.__xtraAttrs__".format(topCtrl), l=True)
        cmds.setAttr("{0}.__xtraAttrs__".format(botCtrl), l=True)

        cmds.addAttr(topCtrl, ln="blink", at="float", dv=0, min=0, max=1, k=True)
        cmds.connectAttr("{0}.blink".format(topCtrl), topBlendAttr)
        cmds.addAttr(botCtrl, ln="blink", at="float", dv=0, min=0, max=1, k=True)
        cmds.connectAttr("{0}.blink".format(botCtrl), botBlendAttr)

        # set up reverse node setup for moving the blink up/down        
        upDownAttr = cmds.addAttr(topCtrl, ln="blendMidDownUp", at="float", dv=0.5, min=0, max=1.0, k=True)
        blinkReverse = cmds.shadingNode("reverse", asUtility=True, name="{0}_blink_reverse".format(self.name))
        cmds.connectAttr("{0}.blendMidDownUp".format(topCtrl), midTopAttr)
        cmds.connectAttr("{0}.blendMidDownUp".format(topCtrl), "{0}.inputX".format(blinkReverse))
        cmds.connectAttr("{0}.outputX".format(blinkReverse), midBotAttr)

        #clean up 
        cmds.setAttr("{0}.blendMidDownUp".format(topCtrl), 0.5)


    def clean_up_rig(self):

        # make middel two ctrls half size
        for side in ["top", "bot"]:
            for ctrl in self.eyeRig[side]["ctrlList"]:
                rig.scale_nurbs_control(ctrl, 0.5, 0.5, 0.5)
            # parent constrain
            for x in [1, 3]:
                ctrl = self.eyeRig[side]["ctrlList"][x]
                rig.scale_nurbs_control(ctrl, 0.5, 0.5, 0.5)
                pc = cmds.parentConstraint([self.eyeRig[side]["ctrlList"][x-1], self.eyeRig[side]["ctrlList"][x+1]], cmds.listRelatives(ctrl, p=True)[0], mo=True)
                rig.assign_color(ctrl, "lightBlue")
#---------------- make attr for constraint? 
        # connect corners xforms
        for x in [0, 4]:
            botBufferGrp = rig.group_freeze(self.eyeRig["bot"]["ctrlList"][x])
            rig.connect_transforms(self.eyeRig["top"]["ctrlList"][x], botBufferGrp, f=True)
            cmds.addAttr(self.eyeRig["top"]["ctrlList"][x], ln="botCornerCtrlVis", at="short", min=0, max=1, dv=0, k=True)
            rig.scale_nurbs_control(self.eyeRig["bot"]["ctrlList"][x], 0.75, 0.75, 0.75)
            cmds.connectAttr("{0}.botCornerCtrlVis".format(self.eyeRig["top"]["ctrlList"][x]), "{0}.v".format(self.eyeRig["bot"]["ctrlList"][x]))

        for side in ["top", "bot"]:
            for ctrl in self.eyeRig[side]["ctrlList"]:
                rig.strip_to_rotate_translate(ctrl)

        if self.blend:
            # create no xform group for eye, move everything including centr and up locs into that
            # create control group 
            # move ctrl grps into that
            pass

        if not self.blend:
            pass

        # # put things in grps
        # # group for no xforms
        # noXformGrp = cmds.group(empty=True, name="{0}_noTransform_GRP".format(self.name))
        # cmds.setAttr("{0}.inheritsTranform".format(noXformGrp), 0)
        # cmds.xform(noXformGrp, ws=True, t=self.centerPos)
        # # group for xforms
        # xformGrp = cmds.group(empty=True, name="{0}_transform_GRP".format(self.name))
        # cmds.xform(xformGrp, ws=True, t=self.centerPos)

        # for crv in 


