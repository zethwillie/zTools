########################
# file: zbw_softDeformer.py
# Author: zeth willie
# Contact: zethwillie@gmail.com, www.williework.blogspot.com
# Date Modified: 05/14/17
# To Use: type in python window  "import zbw_softDeform as zsd; zsd.softDeform()"
# Notes/Descriptions: two tabs- -  1) softMod creates a soft mod w/ a control. If parent obj is not specified,
# it will put rig under geo. 2) softJoint will make (and bind) a joint based on soft selection. will weight joint
# based on soft select weights.
########################


import maya.cmds as cmds
import zTools.rig.zbw_rig as rig
from functools import partial
import maya.mel as mel

widgets = {}

def softDeformerUI():
    """UI for the whole thing"""
# TODO - add some kind of help text to each tab
    if cmds.window("softModWin", exists=True):
        cmds.deleteUI("softModWin")
    widgets["window"] = cmds.window("softModWin", t="zbw_softDeformer", w=300, h=130)
    widgets["tabLO"] = cmds.tabLayout()
    widgets["smCLO"] = cmds.columnLayout("SoftMod", w=300)

    cmds.separator(h=10)
    widgets["smdTFG"] = cmds.textFieldGrp(l="Deformer Name", w=300, cw=[(1, 100), (2, 190)],
                                          cal=[(1, "left"), (2, "left")], tx="softMod_DEF")
    widgets["checkCBG"] = cmds.checkBoxGrp(l="AutoCheck if there are deformers?", v1=1, cw=[(1, 200)],
                                           cal=[(1, "left"), (2, "left")])
    widgets["frontCBG"] = cmds.checkBoxGrp(l="Auto move to front of chain", v1=1, cw=[(1, 200)],
                                           cal=[(1, "left"), (2, "left")])
    widgets["scaleFFG"] = cmds.floatFieldGrp(l="Control Scale", v1=1, pre=2, cw=[(1, 150), (2, 50)],
                                             cal=[(1, "left"), (2, "left")])
    widgets["autoscaleCBG"] = cmds.checkBoxGrp(l="autoscale control?", v1=1, cw=[(1, 200)],
                                           cal=[(1, "left"), (2, "left")])
    widgets["bpFrameIFG"] = cmds.intFieldGrp(l="BindPose/origin Frame", cw=[(1, 150), (2, 50)],
                                             cal=[(1, "left"), (2, "left")])
    widgets["mainCtrlTFBG"] = cmds.textFieldButtonGrp(l="Parent Object:", cw=[(1, 75), (2, 175), (3, 75)], cal=[(1,
                            "left"), (2, "left"), (3, "left")], bl="<<<", bc=partial(set_parent_object, "mainCtrlTFBG"))
    cmds.separator(h=10, style="single")
    widgets["smbutton"] = cmds.button(l="Create Deformer", w=300, h=40, bgc=(.6, .8, .6),
                                    c=partial(create_soft_mod_deformer, False))
    cmds.separator(h=5)
    widgets["wavebutton"] = cmds.button(l="Soft Wave (use falloff to scale wave)", w=300, h=30, bgc=(.8, .8, .6),
                                    c=partial(create_soft_mod_deformer, True))

    # third tab to do softselect to joint
    cmds.setParent(widgets["tabLO"])
    widgets["jointCLO"] = cmds.columnLayout("softJoint", w=300)
    widgets["jntNameTFG"] = cmds.textFieldGrp(l="Joint Name", w=300, cw=[(1, 100), (2, 190)],
                                          cal=[(1, "left"), (2, "left")], tx="softSelect_JNT")
    widgets["jntCPOMCBG"] = cmds.checkBoxGrp(l="Joint to closest point on mesh?", v1=1, cw=[(1, 200)],
                                            cal=[(1, "left"), (2, "left")])
    widgets["jntRotCBG"] = cmds.checkBoxGrp(l="Joint orient to surface?", v1=1, cw=[(1, 200)],
                                            cal=[(1, "left"), (2, "left")])
    widgets["jntAutoCBG"] = cmds.checkBoxGrp(l="Create initial jnt if not bound?", v1=1, cw=[(1, 200)],
                                            cal=[(1, "left"), (2, "left")])
    cmds.separator(h=10)
    widgets["jntbutton"] = cmds.button(l="Create Joint", w=300, h=40, bgc=(.6, .8, .6), c=soft_selection_to_joint)



    cmds.window(widgets["window"], e=True, w=5, h=5, rtf=True)
    cmds.showWindow(widgets["window"])

# --------------------------
# softMod deformer
# --------------------------
# TODO - Add 'wave' to name . . .
def softWave(sftmod, arrow, ctrl,  *args):
    # add values to positions in graph
    positions = [0.0, 0.3, 0.6, 0.9, 0.95]
    values = [1.0, -0.3, 0.1, -0.05, 0.01]
    for i in range(len(positions)):
        cmds.setAttr("{0}.falloffCurve[{1}].falloffCurve_Position".format(sftmod, i), positions[i])
        cmds.setAttr("{0}.falloffCurve[{1}].falloffCurve_FloatValue".format(sftmod, i), values[i])
        cmds.setAttr("{0}.falloffCurve[{1}].falloffCurve_Interp".format(sftmod, i), 2)

    cmds.addAttr(arrow, ln="WaveAttrs", at="enum", k=True)
    cmds.setAttr("{0}.WaveAttrs".format(arrow), l=True)

    # expose these on the control
    for j in range(5):
        cmds.addAttr(arrow, ln="position{0}".format(j), at="float", min=0.0, max=1.0, dv=positions[j], k=True)
        cmds.connectAttr("{0}.position{1}".format(arrow, j),
                         "{0}.falloffCurve[{1}].falloffCurve_Position".format(sftmod, j))

    for j in range(5):
        cmds.addAttr(arrow, ln="value{0}".format(j), at="float", min=-1.0, max=1.0, dv=values[j], k=True)
        cmds.connectAttr("{0}.value{1}".format(arrow, j),
                         "{0}.falloffCurve[{1}].falloffCurve_FloatValue".format(sftmod, j))
        cmds.setAttr("{0}.position{1}".format(arrow, j), l=True)
        cmds.setAttr("{0}.value{1}".format(arrow, j), l=True)


def set_parent_object(tfbg, *args):
    """
    gets selection and puts it in the given text field button grp
    :param tfbg: the key for widget dict for the textFieldButtonGrp
    :param args:
    :return:
    """
    ctrl = None
    sel = cmds.ls(sl=True, type="transform", l=True)
    if sel and (len(sel) == 1):
        ctrl = sel[0]

    if ctrl:
        cmds.textFieldButtonGrp(widgets[tfbg], e=True, tx=ctrl)


def add_top_level_ctrl(origCtrl, type, geo, *args):
    """
    creates a new ctrl, orients it to the geo and parent constrains the orig ctrl rig under itself
    :param origCtrl: the control we're working from
    :param type: the ctrl type of shape see zbw_rig.createControl for options
    :param geo: the geo to orient to
    :param args:
    :return: topCtrl (the new ctrl), grp (the top ctrl grp freeze grp)
    """
    # THIS IS THE XTRA CTRL LAYER, THIS ORIENTS CTRL AND CONNECTS ORIG CTRL TO THE NEW CTRL
    origCtrlPos = cmds.xform(origCtrl, q=True, ws=True, rp=True)
    topCtrl = rig.create_control(name="{0}_moveCtrl".format(origCtrl.rpartition("_")[0]), type=type, axis="z",
                                 color="yellow")
    grp = rig.group_freeze(topCtrl)
    cmds.xform(grp, ws=True, t=origCtrlPos)
    nc = cmds.normalConstraint(geo, grp, worldUpType="vector", upVector=(0, 1, 0))
    cmds.delete(nc)
    pc = cmds.parentConstraint(topCtrl, origCtrl, mo=True)
    sc = cmds.scaleConstraint(topCtrl, origCtrl, mo=True)
    return(topCtrl, grp)


def deformer_check(obj, *args):
    """
    check if there are other deformers on the obj
    :param args:
    :return:
    """
    deformers = rig.get_deformers(obj)
    if deformers:
        cmds.confirmDialog(title='Deformer Alert!',
                           message='Found some deformers on {0}.\nYou may want to put the softmod\n early in the '
                                   'input list\n or check "front of chain"'.format(obj),
                           button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')


def create_soft_mod_deformer(wave=False, *args):
    """
    creates and sets up the softmod deformer
    """
    bpf = cmds.intFieldGrp(widgets["bpFrameIFG"], q=True, v1=True)
    currentTime = cmds.currentTime(q=True)
    cmds.currentTime(bpf)

    check = cmds.checkBoxGrp(widgets["checkCBG"], q=True, v1=True)
    defName = cmds.textFieldGrp(widgets["smdTFG"], tx=True, q=True)
    scaleFactor = cmds.floatFieldGrp(widgets["scaleFFG"], q=True, v1=True)
    front = cmds.checkBoxGrp(widgets["frontCBG"], q=True, v1=True)
    auto = cmds.checkBoxGrp(widgets["autoscaleCBG"], q=True, v1=True)

    if (cmds.objExists(defName)):
        cmds.warning("An object of this name, {0}, already exists! Choose a new name!".format(defName))
        return()

# TODO - check that we've got only verts (or cv's?) selected - always do average?
    vertex = cmds.ls(sl=True, fl=True)
    if not vertex:
        cmds.warning("Must select at least one vertex")
        return()

    # get objects - in no parent object (to parent rig to) then parent to the object itself
    obj = vertex[0].partition(".")[0]

# TODO below is if we have a mesh . . . broaden to nurbs? or curve?
    if cmds.objectType(obj) == "mesh":
        obj = cmds.listRelatives(obj, p=True)[0]
    parentObject = cmds.textFieldButtonGrp(widgets["mainCtrlTFBG"], q=True, tx=True)
    if not parentObject:
        parentObject = obj

    vertPos = rig.average_point_positions(vertex)

    if check and (not front):
        deformer_check(obj)

    cmds.select(obj)
    softMod = defName
    softModAll = cmds.softMod(relative=False, falloffCenter=vertPos, falloffRadius=5.0, n=softMod,
                              frontOfChain=front)
    cmds.rename(softModAll[0], softMod)
    softModXform = cmds.listConnections(softModAll[0], type="transform")[0]

    ctrlName = defName + "_zeroed_GRP"
    control = cmds.group(name=ctrlName, em=True)

# TODO - make a little swatch to set the color of the control
    controlGrp = cmds.group(control, n="{0}_static_GRP".format(control.rpartition("_")[0]))
    cmds.xform(controlGrp, ws=True, t=vertPos)
    if wave:
        ctrlType = "arrow"
    else:
        ctrlType = "cube"
    topCtrl, topGrp = add_top_level_ctrl(control, ctrlType, cmds.listRelatives(obj, s=True)[0])

# TODO figure out how to transpose the space for just the scale
    rig.connect_transforms(control, softModXform)

    cmds.addAttr(topCtrl, ln="__XTRA__", at="enum", k=True)
    cmds.setAttr("{0}.__XTRA__".format(topCtrl), l=True)
    cmds.addAttr(topCtrl, ln="envelope", at="float", min=0, max=1, k=True, dv=1)
    cmds.addAttr(topCtrl, ln="falloff", at="float", min=0, max=100, k=True, dv=5)
    cmds.addAttr(topCtrl, ln="mode", at="enum", enumName= "volume=0:surface=1", k=True)

    # connect that attr to the softmod falloff radius
    cmds.connectAttr("{0}.envelope".format(topCtrl), "{0}.envelope".format(softMod))
    cmds.connectAttr("{0}.falloff".format(topCtrl), "{0}.falloffRadius".format(softMod))
    cmds.connectAttr("{0}.mode".format(topCtrl), "{0}.falloffMode".format(softMod))
    cmds.setAttr("{0}.inheritsTransform".format(softModXform), 0)
    cmds.setAttr("{0}.visibility".format(softModXform), 0)

    if auto:
        calsz = rig.calibrate_size(obj, .15)
        if calsz:
            rig.scale_nurbs_control(topCtrl, calsz, calsz, calsz)
            cmds.setAttr("{0}.falloff".format(topCtrl), 2*calsz)
        else:
            cmds.warning("I had an issue getting the calibrated scale of {0}".format(obj))
    rig.scale_nurbs_control(topCtrl, scaleFactor, scaleFactor, scaleFactor)

    defGroup = cmds.group(empty=True, n=(defName + "_deform_GRP"))
    cmds.xform(defGroup, ws=True, t=vertPos)
    cmds.parent(softModXform, controlGrp, defGroup)

# TODO - use the name of the deformer instead. . .
    masterGrp = cmds.group(name="{0}_mstr_GRP".format(obj), em=True)
    cmds.parent(topGrp, defGroup, masterGrp)

    if wave:
        softWave(softMod, topCtrl, control)

    cmds.parent(masterGrp, parentObject)

    newName = rig.increment_name(defName)
    cmds.textFieldGrp(widgets["smdTFG"], tx=newName, e=True)

    cmds.select(topCtrl)
    cmds.currentTime(currentTime)

    return (softMod, control, obj, defGroup)


#########
# joint stuff
#########
def soft_selection_to_joint(*args):
    """
    takes a soft selection of verts and creates a joint to bind & wieght them in that proportion
    :param args:
    :return: string - name of the soft sel joint we've created
    """
# TODO - check for selection of verts!
    selVtx = cmds.ls(sl=True, fl=True) # to get center for joint
    vtxs, wts = rig.get_soft_selection() # to get weights for jnt

    tform = vtxs[0].partition(".")[0]
    mesh = cmds.listRelatives(tform, s=True)[0]
    ptOnSurface = cmds.checkBoxGrp(widgets["jntCPOMCBG"], q=True, v1=True)
    auto = cmds.checkBoxGrp(widgets["jntAutoCBG"], q=True, v1=True)
    jntName = cmds.textFieldGrp(widgets["jntNameTFG"], q=True, tx=True)
    rotOnSurface = cmds.checkBoxGrp(widgets["jntRotCBG"], q=True, v1=True)

    cls = mel.eval("findRelatedSkinCluster " + tform)
    if not cls:
        if auto:
            baseJnt, cls = rig.new_joint_bind_at_center(tform)
        else:
            cmds.warning("There isn't an initial bind on this geometry. Either create one or check 'auto'")
            return()

    center = rig.average_point_positions(selVtx)
    rot = (0,0,0)
    if ptOnSurface:
        center = rig.closest_point_on_mesh_position(center, mesh)
    if rotOnSurface:
        rot = rig.closest_point_on_mesh_rotation(center, mesh)

    cmds.select(cl=True)
    jnt = cmds.joint(name = jntName)
    cmds.xform(jnt, ws=True, t=center)
    cmds.xform(jnt, ws=True, ro=rot)

    # add influence to skin Cluster
    cmds.select(tform, r=True)
    cmds.skinCluster(e=True, ai=jnt, wt=0)

    # apply weights to that joint
    for v in range(len(vtxs)):
        cmds.skinPercent(cls, vtxs[v], transformValue=[jnt, wts[v]])

    newName = rig.increment_name(jntName)
    cmds.textFieldGrp(widgets["jntNameTFG"], tx=newName, e=True)

    return(jnt)


def softDeformer():
    """Use this to start the script!"""
    softDeformerUI()
