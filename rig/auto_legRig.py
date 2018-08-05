import maya.cmds as cmds

import python_rigger_old.rigger_tools.rigger_tools as zrt

reload(zrt)
import zTools.rig.auto_baseLimb as BL

reload(BL)
import zTools.rig.zbw_rig as rig

reload(rig)
import zTools.rig.auto_rigWindow as zrw

reload(zrw)


class LegRigUI(zrw.RiggerWindow):
    def __init__(self):
        self.width = 300
        self.height = 600

        self.winInitName = "zbw_legRiggerUI"
        self.winTitle = "Leg Rigger UI"
        # common
        self.defaultLimbName = "leg"
        self.defaultOrigPrefix = "L"
        self.defaultMirPrefix = "R"
        self.pts = [(5, 12, 0), (5, 7, 1), (5, 2, 0), (5, 1, 3), (5, 1, 4)]
        self.baseNames = ["thigh", "knee", "ankle", "ball", "ballEnd"]
        self.secRotOrderJnts = []
        self.ikShape = "box"
        self.make_UI()

    def create_rigger(self, *args):
        self.rigger = LegRig()
        self.get_values_for_rigger()
        self.set_values_for_rigger()


class LegRig(BL.BaseLimb):
    def __init__(self):
        BL.BaseLimb.__init__(self)
        # can add this in tht ui? need to?
        self.revFootPts = [(5, 1, 3), (5, 0, 4), (5, 0, -2)]

        self.revFootNames = ["ball", "toe", "heel"]
        self.revFootLocs = {"orig": [], "mir": []}
        self.footPivots = {}
        self.ikShape = "box"
        self.ikOrient = False
        self.reverseFootBallCtrls = {"orig": None, "mir": None}

    def pose_initial_joints(self):
        BL.BaseLimb.pose_initial_joints(self)
        # need to work on orienting the joints here. . . which attrs to lock (just unlock all?)
        for i in range(len(self.revFootNames)):
            loc = \
            cmds.spaceLocator(name="{0}_LOC".format(self.revFootNames[i]))[0]
            cmds.xform(loc, ws=True, t=self.revFootPts[i])
            self.revFootLocs["orig"].append(loc)
            # cmds.parent(self.revFootLocs[0], self.joints[2])
            # cmds.parent(self.revFootLocs[1:], self.revFootLocs[0])

    def make_limb_rig(self):
        self.clean_initial_joints()
        # add manual adjust joint orientation here. . .
        if self.mirror:
            self.mirror_joints()
        self.setup_dictionaries()
        self.create_duplicate_chains()
        self.create_fk_rig()
        self.create_fkik_switch()
        self.connect_deform_joints()
        self.create_ik_rig()
        self.create_ik_stretch()
        self.create_rigSide_groups()
        if self.twist:
            self.create_twist_extraction_rig()
        self.create_ik_group()
        self.create_reverse_foot()
        self.clean_up_rig()
        self.create_sets()
        self.label_deform_joints()

    def create_reverse_foot(self):
        mirrorScale = (1, 1, 1)
        if self.mirror:
            if self.mirrorAxis == "yz":
                mirrorScale = (-1, 1, 1)
            elif self.mirrorAxis == "xy":
                mirrorScale = (1, 1, -1)
            elif self.mirrorAxis == "xz":
                mirrorScale = (1, -1, 1)
            for loc in self.revFootLocs["orig"]:
                cmds.xform(loc, ws=True, sp=(0, 0, 0))
                dupe = cmds.duplicate(loc)[0]
                cmds.xform(dupe, s=mirrorScale)
                self.revFootLocs["mir"].append(dupe)

        for side in self.fkJoints.keys():
            if side == "orig":
                sideName = self.origPrefix
            if side == "mir":
                sideName = self.mirPrefix
            self.footPivots[side] = []

            # add attrs to ankle ctrl
            cmds.addAttr(self.ikCtrls[side][0], ln="__RevFootAttrs__",
                         at="enum", en="-----", k=True)
            cmds.setAttr("{0}.__RevFootAttrs__".format(self.ikCtrls[side][0]),
                         l=True)
            rollAttrs = ["ballRoll", "toeRoll", "heelRoll"]
            twistAttrs = ["ballTwist", "toeTwist", "heelTwist"]
            for attr in rollAttrs:
                cmds.addAttr(self.ikCtrls[side][0], ln=attr, at="float", dv=0.0,
                             k=True)
            for attr in twistAttrs:
                cmds.addAttr(self.ikCtrls[side][0], ln=attr, at="float", dv=0.0,
                             k=True)
            cmds.addAttr(self.ikCtrls[side][0], ln="toeFlap", at="float",
                         dv=0.0, k=True)

            # create grp for each loc
            for loc in self.revFootLocs[side]:
                grp = cmds.group(em=True,
                                 name="{0}_{1}_{2}".format(sideName, self.part,
                                                           loc.replace("LOC",
                                                                       "PIV")))
                pos = cmds.pointPosition(loc)
                cmds.xform(grp, ws=True, t=pos)
                self.footPivots[side].append(grp)

            # parent ball to toe, toe to heel, heel to to ctrl
            cmds.parent(self.footPivots[side][0], self.footPivots[side][1])
            cmds.parent(self.footPivots[side][1], self.footPivots[side][2])
            cmds.parent(self.footPivots[side][2], self.ikCtrls[side][0])

            # parent ik to ball grp
            cmds.parent(self.ikHandles[side][0], self.footPivots[side][0])
            # create new ik from ankle to ball, parent under 
            ikName = "{0}_{1}_ballIK".format(sideName, self.part)
            ballHandle = cmds.ikHandle(startJoint=self.ikJoints[side][2],
                                       endEffector=self.ikJoints[side][3],
                                       name=ikName, solver="ikRPsolver")[0]
            self.ikHandles[side].append(ballHandle)
            cmds.parent(ballHandle, self.footPivots[side][0])
            cmds.setAttr("{0}.visibility".format(ballHandle), 0)
            # create ctrl at ball, grpFreeze, orient constrain ikBall to this
            ballCtrl, ballGrp = zrt.create_control_at_joint(
                self.ikJoints[side][3], "circle", "x",
                "{0}_ball_{1}".format(sideName, self.ctrlSuffix),
                self.groupSuffix, orient=True)
            cmds.setAttr("{0}.v".format(ballCtrl), 0)
            self.reverseFootBallCtrls[side] = ballCtrl
            cmds.parent(ballGrp, self.footPivots[side][1])
            # connect attrs
            for i in range(len(rollAttrs)):
                cmds.connectAttr(
                    "{0}.{1}".format(self.ikCtrls[side][0], rollAttrs[i]),
                    "{0}.rx".format(self.footPivots[side][i]))
                cmds.connectAttr(
                    "{0}.{1}".format(self.ikCtrls[side][0], twistAttrs[i]),
                    "{0}.ry".format(self.footPivots[side][i]))
            cmds.connectAttr("{0}.toeFlap".format(self.ikCtrls[side][0]),
                             "{0}.rz".format(self.reverseFootBallCtrls[side]))
            # delete pv locs
            cmds.delete(self.revFootLocs[side])

            # connect pv to foot, follow attr etc

    def clean_up_rig(self):
        BL.BaseLimb.clean_up_rig(self)
        for side in self.fkJoints.keys():
            cmds.setAttr("{0}.fkik".format(self.switchCtrls[side]), 1)
