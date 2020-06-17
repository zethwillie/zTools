import maya.cmds as cmds
import json
import os
from functools import partial
import zTools.rig.zbw_rig as rig
reload(rig)
import zTools.zbw_tools as tools
reload(tools)


# add cylinders for each joint weighted to 1, then combine them WITH skin clusters
# add another button to create proxy geo 
# add another button to bind the simple geometry

# come up with a more elegant way to deal with joint/ctrl stuff. Maybe expand out to rig class stuff? Or bring that into here? 
# add joint orient to window? for control creation
# add ik to fingers?


'''
# to serialize info
sel = cmds.ls(sl=True)

joint_dictionary = {}

for jnt in sel:
    name = jnt
    par = cmds.listRelatives(jnt, parent=True)
    if par:
        par = par[0]
    trans = cmds.xform(jnt, q=True, ws=True, t=True)
    rot = cmds.xform(jnt, q=True, ws=True, ro=True)
    scl = cmds.xform(jnt, q=True, ws=True, s=True)
    jo = cmds.joint(jnt, q=True, orientation=True)
    side = cmds.getAttr("{0}.side".format(jnt))
    part = cmds.getAttr("{0}.type".format(jnt))
    joint_dictionary[name] = {"parent":par, "translate":trans, "rotation":rot, "scale":scl, "orientation":jo, "side":side, "part":part}

with open(r'c://users/zeth/Desktop/handData.txt', 'w') as outfile:
    json.dump(joint_dictionary, outfile)
'''

class HandRig(object):
    def __init__(self):
        self.joint_dictionary = {}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open("{0}/handData.json".format(dir_path)) as json_file:
            data = json.load(json_file)
            self.joint_dictionary = data

        self.allJoints = []
        self.proxyList = []
        self.proxyJnts = []

        self.hand_rig_UI()

    def hand_rig_UI(self):
        if cmds.window("handWin", exists=True):
            cmds.deleteUI("handWin")

        self.win = cmds.window("handWin", t="zbw_hand_rig", w=280)
        cmds.columnLayout()
        self.mirror = cmds.checkBoxGrp(l="Mirror: ", ncb=1, v1=True, cal=[(1,"left"),(2,"left")], cw=[(1, 50), (2,20)])
        cmds.text("Create joints, orient them, then click rig")
        cmds.button(l="Import Joints", w=280, h=50, bgc=(.7, .5, .5), c=self.joint_setup)
        cmds.separator(h=10)
        cmds.button(l="Rig Joints", w=280, h=50, bgc=(.5, .7, .5), c=self.build_rig)
        cmds.button(l="Create Proxy Geo", w=280, h=50, bgc=(.5, .5, .7), c=self.create_proxy)
        cmds.button(l="Bind Proxy Geo", w=280, h=50, bgc=(.7, .7, .5), c=self.prep_bind)

        cmds.showWindow(self.win)
        cmds.window(self.win, e=True, rtf=True)


    def joint_setup(self, *args):
        for jnt in self.joint_dictionary.keys():
            cmds.select(cl=True)
            cmds.joint(name=jnt, position=self.joint_dictionary[jnt]["translate"], a=True)

        for jnt in self.joint_dictionary.keys():
            cmds.xform(jnt, ws=True, ro=self.joint_dictionary[jnt]["rotation"])

        for jnt in self.joint_dictionary.keys():
            cmds.select(cl=True)
            try:
                cmds.parent(jnt, self.joint_dictionary[jnt]["parent"])
            except:
                pass

        for jnt in self.joint_dictionary.keys():
            if jnt == "hand_JNT":
                continue
            jo = self.joint_dictionary[jnt]["orientation"]
            cmds.setAttr("{0}.jointOrient".format(jnt), jo[0], jo[1], jo[2])
            
        for jnt in self.joint_dictionary.keys():
            cmds.makeIdentity(jnt)


    def build_rig(self, *args):
        colors = ["lightBlue", "pink", "darkBlue", "darkRed"]
        self.mirrored = cmds.checkBoxGrp(self.mirror, q=True, v1=True)

        if self.mirrored:
            sides = ["lf", "rt"]
        else:
            sides = ["lf"]
        self.sideJnts = []

        # figure out which joints we have kept
        culledJnts = []
        for jnt in self.joint_dictionary.keys():
            if cmds.objExists(jnt):
                culledJnts.append(jnt)
        
        self.leftJoints = [cmds.rename(x, "lf_{0}".format(x)) for x in culledJnts]
        self.sideJnts.append(self.leftJoints)
        if self.mirrored:
            self.rightJoints = cmds.mirrorJoint("lf_hand_JNT", mirrorBehavior=True, mirrorYZ=True, searchReplace = ["lf", "rt"])
            self.sideJnts.append(self.rightJoints)
        
        self.bindJoints = []
        # build rig for sides
        for x in range(len(sides)):
            sideJntsComplete = []
            sideCtrl = rig.create_control("ctrl", "lollipop", "y", colors[x])
            if x == 1:
                self.reverse_control(sideCtrl)
            rig.scale_nurbs_control(sideCtrl, .2, .2, .2)
            
            # get rid of end joints
            for z in range(len(self.sideJnts[x])):
                if "End" not in self.sideJnts[x][z]:
                    sideJntsComplete.append(self.sideJnts[x][z])

            # connect jnts and ctrls
            cmds.select(sideCtrl, r=True)
            cmds.select(sideJntsComplete, add=True)
            ctrls, grps = tools.freeze_and_connect()

            # rename ctrls to get rid of "JNT"
            cmds.select("{0}_hand_JNTCtrl_GRP".format(sides[x]), r=True)
            cmds.select(hi=True)
            ctrlList = []
            sel = cmds.ls(sl=True)        
            sel.reverse()
            list(set(sel))
            for y in sel:
                newCtrlObj = cmds.rename(y, y.replace("JNT", ""))
                ctrlList.append(newCtrlObj)
            
            # hide hand ctrl
            topShp = cmds.listRelatives("{0}_hand_Ctrl".format(sides[x]), s=True)[0]
            cmds.setAttr("{0}.v".format(topShp), 0)

# additional offset for attr ctrl of indiv finger joints? 
            # create offset grps on ctrls
            for ctrl in ctrlList:
                shp = cmds.listRelatives(ctrl, s=True)
                if shp:
                    if cmds.objectType(shp)=="nurbsCurve":
                        offsetGrp = rig.group_freeze(ctrl, "offset")

            # create top groups for the left controls
            ctrlGrp = cmds.group("{0}_hand_Ctrl_GRP".format(sides[x]), name="{0}_hand_GRP".format(sides[x]))
            handPos = cmds.xform("{0}_hand_Ctrl_GRP".format(sides[x]), q=True, ws=True, rp=True)
            cmds.xform(ctrlGrp, ws=True, preserve=True, rp=handPos)
            attachGrp = cmds.group(ctrlGrp, name="{0}_hand_attach_GRP".format(sides[x]))
            cmds.xform(attachGrp, ws=True, preserve=True, rp=handPos)

            # create auto ctrls
            autoCtrl = rig.create_control("{0}_hand_auto_CTRL".format(sides[x]), "circle", "y", colors[x+2])
            autoGrp = rig.group_freeze(autoCtrl)
            rig.snap_to("{0}_hand_Ctrl_GRP".format(sides[x]), autoGrp)
            cmds.parent(autoGrp, "{0}_hand_Ctrl".format(sides[x]))
            cmds.xform(autoGrp, ws=True, r=True, t=(0, 1, 0))
            rig.strip_transforms(autoCtrl)
            for attr in ["relaxed", "fist", "spread", "claw", "point"]:
                cmds.addAttr(autoCtrl, ln=attr, at="float", min=0, max=10, dv=0, k=True)


            for a in sideJntsComplete:
                if "hand" not in a:
                    self.allJoints.append(a)


    def reverse_control(self, ctrl=None):
        cmds.setAttr("{0}.rz".format(ctrl), 180)
        cmds.makeIdentity(ctrl, apply=True)


    def create_proxy(self, *args):
        proxyGrp = cmds.group(em=True, name="hand_proxy_GRP")
        geoList = []
        jntList = []
        for x in self.leftJoints:
            # get rid of End jnts
            if "End" not in x:
                proxy = self.create_cylinder(x)
                rig.snap_to(x, proxy)
                cmds.parent(proxy, proxyGrp)
                geoList.append(proxy)
                jntList.append(x)
        self.proxyList = geoList
        self.proxyJnts = jntList


    def create_cylinder(self, jnt, *args):
        # create cylinder
        cyl = cmds.polyCylinder(name="{0}_proxy_geo".format(jnt), axis=(1,0,0))[0]
        # move pivot to origin
        cmds.xform(cyl, ws=True, a=True, rp=[0,0,0])
        return(cyl)

    def prep_bind(self, *args):
        self.bind_proxy(self.proxyJnts, self.proxyList)


    def bind_proxy(self, jntList, geoList, *args):
        # bind geo to the associated joint

        for x in range(len(jntList)):
            cmds.skinCluster(jntList[x], geoList[x], bindMethod=0, skinMethod=0, normalizeWeights=1, maximumInfluences=1, obeyMaxInfluences=True, tsb=True)

        combined = cmds.polyUniteSkinned(geoList, ch=0, mergeUVSets=True, centerPivot=True)[0]
        proxyCombined = cmds.rename(combined, "proxyCombined_GEO")