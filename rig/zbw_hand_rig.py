import maya.cmds as cmds
import json
import os
import zTools.rig.zbw_rig as rig
reload(rig)

# SHOULD I ADD IN THE GEO AND SKIN WEIGHTING SO i CAN PASS THAT ON?
# add joint orient to window? for control creation
# add ik to fingers
# add groups to controls to autodrive them, add attrs w values or preset sdk
# create control for above
# move groups to hand joint
# encapsulate this for reversed hand


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

        self.hand_rig_UI()

    def hand_rig_UI(self):
        if cmds.window("handWin", exists=True):
            cmds.deleteUI("handWin")

        self.win = cmds.window("handWin", t="zbw_hand_rig", w=280)
        cmds.columnLayout()
        cmds.text("Create joints, orient them, then click rig")
        cmds.button(l="Import Joints", w=280, h=50, bgc=(.7, .5, .5), c=self.joint_setup)
        cmds.separator(h=10)
        cmds.button(l="Rig Joints", w=280, h=50, bgc=(.5, .7, .5), c=self.build_rig)

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
            
        # here we pause to move and orient joints

    def build_rig(self, *args):
        # make all of these encapsulated
        self.leftJoints = [cmds.rename(x, "lf_{0}".format(x)) for x in self.joint_dictionary.keys()]
        # create and add controls for left
        lfCtrl = rig.create_control("ctrl", "lollipop", "y", "royalBlue")
        rig.scale_nurbs_control(lfCtrl, .2, .2, .2)
        cmds.select(lfCtrl, r=True)
        cmds.select(self.leftJoints, add=True)

        ctrls, grps = tools.freeze_and_connect()
        cmds.select("lf_hand_JNTCtrl_GRP", r=True)
        cmds.select(hi=True)
        self.lfCtrlList = []
        sel = cmds.ls(sl=True)        
        sel.reverse()
        list(set(sel))
        for x in sel:
            newCtrlObj = cmds.rename(x, x.replace("JNT", ""))
            self.lfCtrlList.append(newCtrlObj)
        # create a group for the left controls
        self.lfCtrlGrp = cmds.group("lf_hand_Ctrl_GRP", name="lf_hand_GRP")
        self.lfAttachGrp = cmds.group(self.lfCtrlGrp, name="lf_hand_attach_GRP")
