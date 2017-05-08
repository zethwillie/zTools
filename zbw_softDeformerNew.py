########################
# file: zbw_softDeformer.py
# Author: zeth willie
# Contact: zethwillie@gmail.com, www.williework.blogspot.com
# Date Modified: 05/03/17
# To Use: type in python window  "import zbw_softDeform as zsd; zsd.softDeform()"
# Notes/Descriptions: two tabs to create two different deformers. . . 1. softMod deformer - creates a soft mod deformer at the selected verts and encapsulates it in two controls. One moves the center of deformation, the other moves the actual soft mod. 2. creates an anim control on a soft selection
########################


import maya.cmds as cmds
import zTools.zbw_rig as rig
import zTools.mayaDecorators as decor

widgets = {}


def softDeformerUI():
    """UI for the whole thing"""
    if cmds.window("softModWin", exists=True):
        cmds.deleteUI("softModWin")
    widgets["window"] = cmds.window("softModWin", t="zbw_softDeformer", w=300, h=130)
    widgets["tabLO"] = cmds.tabLayout()
    widgets["smCLO"] = cmds.columnLayout("SoftModDeformer", w=300)

    cmds.separator(h=10)
    widgets["smdTFG"] = cmds.textFieldGrp(l="Deformer Name", w=300, cw=[(1, 100), (2, 190)],
                                          cal=[(1, "left"), (2, "left")], tx="softMod_DEF")
    widgets["firstVertCBG"] = cmds.checkBoxGrp(l="Use only 1st vert (vs. avg pos)", v1=0, cw=[(1, 200)],
                                               cal=[(1, "left"), (2, "left")])
    widgets["parentCBG"] = cmds.checkBoxGrp(l="Parent Ctrl Under Geo?", v1=0, cw=[(1, 200)],
                                            cal=[(1, "left"), (2, "left")])
    widgets["incrCBG"] = cmds.checkBoxGrp(l="Increment name after creation?", v1=1, cw=[(1, 200)],
                                          cal=[(1, "left"), (2, "left")])
    widgets["checkCBG"] = cmds.checkBoxGrp(l="AutoCheck if there are deformers?", v1=1, cw=[(1, 200)],
                                           cal=[(1, "left"), (2, "left")])
    widgets["scaleFFG"] = cmds.floatFieldGrp(l="Control Scale", v1=1, pre=2, cw=[(1, 100), (2, 50)],
                                             cal=[(1, "left"), (2, "left")])
    widgets["bpFrameIFG"] = cmds.intFieldGrp(l="Bind Pose Frame", cw=[(1, 100), (2, 50)],
                                             cal=[(1, "left"), (2, "left")])
    # widgets["mainCtrlTFBG"] = cmds.textFieldButtonGrp(l="main control", cw=[(1, 75), (2, 175), (3, 75)],
    #                                                  cal=[(1, "left"), (2, "left"), (3, "left")], bl="<<<",
    # bc=getCtrl)

    cmds.separator(h=10, style="single")
    widgets["button"] = cmds.button(l="Create Deformer", w=300, h=40, bgc=(.6, .8, .6), c=create_soft_mod_deformer)
    # widgets["button"] = cmds.button(l="Soft Wave (scale to drive falloff)", w=300, h=40, bgc=(.8, .8, .6), c=softWave)

    # second tab to softselect deformer
    cmds.setParent(widgets["tabLO"])
    widgets["ssCLO"] = cmds.columnLayout("SoftSelectDeformer", w=300)
    widgets["ssdTFG"] = cmds.textFieldGrp(l="Deformer Name", w=300, cw=[(1, 100), (2, 190)],
                                          cal=[(1, "left"), (2, "left")], tx="softSelect_DEF")
    widgets["ssCPOMCBG"] = cmds.checkBoxGrp(l="Control to closest point on mesh?", v1=1, cw=[(1, 200)],
                                            cal=[(1, "left"), (2, "left")])
    widgets["ssParentCBG"] = cmds.checkBoxGrp(l="Parent Ctrl Under Geo?", v1=0, cw=[(1, 200)],
                                              cal=[(1, "left"), (2, "left")])
    widgets["ssIncrCBG"] = cmds.checkBoxGrp(l="Increment name after creation?", v1=1, cw=[(1, 200)],
                                            cal=[(1, "left"), (2, "left")])
    widgets["ssCheckCBG"] = cmds.checkBoxGrp(l="AutoCheck if there are deformers?", v1=1, cw=[(1, 200)],
                                             cal=[(1, "left"), (2, "left")])
    widgets["ssScaleFFG"] = cmds.floatFieldGrp(l="Control Scale", v1=1, pre=2, cw=[(1, 100), (2, 50)],
                                               cal=[(1, "left"), (2, "left")])
    cmds.separator(h=10, style="single")
    widgets["button"] = cmds.button(l="Create Deformer", w=300, h=40, bgc=(.6, .8, .6), c=softSelectDef)

    cmds.showWindow(widgets["window"])


# --------------------------
# softMod deformer
# --------------------------

@decor.d_unifyUndo
def softWave(*args):
    bpf = cmds.intFieldGrp(widgets["bpFrameIFG"], q=True, v1=True)
    currentTime = cmds.currentTime(q=True)
    cmds.currentTime(bpf)

    sftmod, ctrl, geo, defGroup = create_soft_mod_deformer()

    main = cmds.textFieldButtonGrp(widgets["mainCtrlTFBG"], q=True, tx=True)
    if not main:
        cmds.warning("You need to have a main control selected to hook things up!")
        return ()

    if not cmds.objExists("{0}_waveDeformer_GRP".format(geo)):
        waveGrp = cmds.group(name="{0}_waveDeformer_GRP".format(geo), em=True)
    p = cmds.listRelatives("{0}_waveDeformer_GRP".format(geo), p=True)
    if not p:
        cmds.parent("{0}_waveDeformer_GRP".format(geo), main)

    ctrlPos = cmds.xform(ctrl, q=True, ws=True, rp=True)
    arrow = rig.createControl(name="{0}_ptrCtrl".format(ctrl), type="arrow", axis="z", color="yellow")
    grp = rig.groupFreeze(arrow)
    cmds.xform(grp, ws=True, t=ctrlPos)
    nc = cmds.normalConstraint(geo, grp)
    cmds.delete(nc)
    pc = cmds.parentConstraint(arrow, ctrl, mo=True)

    # hide control
    cmds.setAttr("{0}.v".format(ctrl), 0)
    # add values to positions in graph
    positions = [0.0, 0.3, 0.6, 0.9, 0.95]
    values = [1.0, -0.3, 0.1, -0.05, 0.01]
    for i in range(len(positions)):
        cmds.setAttr("{0}.falloffCurve[{1}].falloffCurve_Position".format(sftmod, i), positions[i])
        cmds.setAttr("{0}.falloffCurve[{1}].falloffCurve_FloatValue".format(sftmod, i), values[i])
        cmds.setAttr("{0}.falloffCurve[{1}].falloffCurve_Interp".format(sftmod, i), 2)

    # connect falloff
    mult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_mult".format(ctrl))
    cmds.setAttr("{0}.input2".format(mult), 5, 5, 5)
    cmds.connectAttr("{0}.scale".format(arrow), "{0}.input1".format(mult))
    cmds.connectAttr("{0}.outputX".format(mult), "{0}.falloff".format(ctrl))

    cmds.addAttr(arrow, ln="WaveAttrs", at="enum", k=True)
    cmds.addAttr(arrow, ln="waveStrength", at="float", min=0, max=1, dv=1, k=True)
    cmds.setAttr("{0}.WaveAttrs".format(arrow), l=True)
    cmds.connectAttr("{0}.waveStrength".format(arrow), "{0}.envelope".format(ctrl))

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

    # group the whole thing
    cmds.parent(defGroup, grp)
    cmds.parent(grp, "{0}_waveDeformer_GRP".format(geo))
    cmds.currentTime(currentTime)

# ---------------- get list of all softMod defs, then figure out how to pop these into the front of the deformer stack

def getCtrl(*args):
    ctrl = None
    sel = cmds.ls(sl=True, type="transform")
    if sel and (len(sel) == 1):
        ctrl = sel[0]

    if ctrl:
        cmds.textFieldButtonGrp(widgets["mainCtrlTFBG"], e=True, tx=ctrl)


# TODO option to throw deformer to front of chain? (should just be arg in deformer creation)
def create_soft_mod_deformer(*args):
    """
    creates and sets up the softmod deformer
    """
    check = cmds.checkBoxGrp(widgets["checkCBG"], q=True, v1=True)
    increment = cmds.checkBoxGrp(widgets["incrCBG"], q=True, v1=True)
    toParent = cmds.checkBoxGrp(widgets["parentCBG"], q=True, v1=True)
    # get deformer name
    defName = cmds.textFieldGrp(widgets["smdTFG"], tx=True, q=True)
    scaleFactor = cmds.floatFieldGrp(widgets["scaleFFG"], q=True, v1=True)

    if (cmds.objExists(defName)):
        cmds.warning("An object of this name, {0}, already exists! Choose a new name!".format(defName))
        return()

# TODO - check that we've got only verts (or cv's?) selected
    vertsRaw = cmds.ls(sl=True, fl=True)

    if not vertsRaw:
        cmds.warning("Must select at least one vertex")
        return()
    else:
        if (cmds.checkBoxGrp(widgets["firstVertCBG"], q=True, v1=True)):
            vertex = [vertsRaw[0]]
        else:
            vertex = vertsRaw

    obj = vertex[0].partition(".")[0]

    # get vert position then select the geo
    positions = []
    for vert in vertex:
        positions.append(cmds.pointPosition(vert))

    vertPos = rig.average_vectors(positions)

    # check if there are other deformers on the obj
    if check:
        deformers = getDeformers(obj)
        if deformers:
            cmds.confirmDialog(title='Deformer Alert!',
                               message='Found some deformers on %s.\nYou may want to put the softmod\n early in the input list' % obj,
                               button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')

    cmds.select(obj)

    # create a soft mod at vert position (avg)
# TODO - generalize the name bit - create a passthrough function that parses stuff
    softMod = defName
    softModAll = cmds.softMod(relative=False, falloffCenter=vertPos, falloffRadius=5.0, n=softMod,
                              frontOfChain=True)

    cmds.rename(softModAll[0], softMod)
    softModXform = cmds.listConnections(softModAll[0], type="transform")[0]

    # create a control at the position of the softmod
    control = defName + "_CTRL"
    rig.createControl(name=control, axis="x", type="sphere", color="red")
# TODO - pick a random color choice for this control - later on make a little swatch to set the color of the control

    controlGrp = cmds.group(control, n="{0}_GRP".format(control))
    cmds.xform(controlGrp, ws=True, t=vertPos)

    # connect the pos, rot, scale of the control to the softModHandle
    rig.connect_transforms(control, softModXform)

    cmds.addAttr(control, ln="__XTRA__", at="enum", k=True)
    cmds.setAttr("{0}.__XTRA__".format(control), l=True)

    cmds.addAttr(control, ln="envelope", at="float", min=0, max=1, k=True, dv=1)
    cmds.addAttr(control, ln="falloff", at="float", min=0, max=100, k=True, dv=5)
    cmds.addAttr(control, ln="mode", at="enum", enumName= "volume=0:surface=1", k=True)

    # connect that attr to the softmod falloff radius
    cmds.connectAttr("{0}.envelope".format(control), "{0}.envelope".format(softMod))
    cmds.connectAttr("{0}.falloff".format(control), "{0}.falloffRadius".format(softMod))
    cmds.connectAttr("{0}.mode".format(control), "{0}.falloffMode".format(softMod))

    cmds.setAttr("{0}.inheritsTransform".format(softModXform), 0)

    cmds.setAttr("{0}.visibility".format(softModXform), 0)

    # group the group and the softmod xform
    defGroup = cmds.group(empty=True, n=(defName + "_deform_GRP"))
    cmds.xform(defGroup, ws=True, t=vertPos)
    cmds.parent(softModXform, controlGrp, defGroup)

# TODO - make a text field button group to get this. if it's blank parent to world (or not at all)
    if toParent:
        cmds.parent(defGroup, obj)

    rig.scale_nurbs_control(control, scaleFactor, scaleFactor, scaleFactor)

# TODO - write incremenet name function in zbw_rig
    # increment name
    if increment:
        newName = rig.increment_name(defName)
        cmds.textFieldGrp(widgets["smdTFG"], tx=newName, e=True)

    # select the control to wrap up
    cmds.select(control)
    return (softMod, control, obj, defGroup)


# --------------------------
# softSelection deformer
# --------------------------

# TO-DO----------------checks on whether a) something is selected b) vertices are selected
def softSelectDef(*args):
    """
    calls on get_soft_selection() to get the weights of the softSelect and then puts it all under a cluster and a control
    """
# TODO - see what we can use from above script down here. . . Then we can reuse maybe for the other two (joints, wave)
    ssDefName = cmds.textFieldGrp(widgets["ssdTFG"], q=True, tx=True)

    if cmds.objExists("{0}_CLS".format(ssDefName)):
        cmds.warning("An object/cluster of that name already exists! Please choose another name!")
        return()

    ssScale = cmds.floatFieldGrp(widgets["ssScaleFFG"], q=True, v1=True)
    ssIncrement = cmds.checkBoxGrp(widgets["ssIncrCBG"], q=True, v1=True)
    ssCheck = cmds.checkBoxGrp(widgets["ssCheckCBG"], q=True, v1=True)
    ssParent = cmds.checkBoxGrp(widgets["ssParentCBG"], q=True, v1=True)
    ssCPOM = cmds.checkBoxGrp(widgets["ssCPOMCBG"], q=True, v1=True)

    # this gets the verts selected and their respective weights in the soft selection
    elements, weights = rig.get_soft_selection()
    if not elements:
        cmds.warning("zbw_softDeformere.softSelectDef: There was a problem getting the soft selection!")
        return()

    # get transform and mesh
    xform = elements[0].partition(".")[0]
    # maybe here I should check for "orig", etc and exclude them?
    mesh = cmds.listRelatives(xform, f=True, s=True)[0]

    # check if there are other deformers on the obj
    if ssCheck:
        deformers = []
        deformers = getDeformers(xform)
        if deformers:
            cmds.confirmDialog(title='Deformer Alert!',
                               message='Found some deformers on %s.\nYou may want to put the softmod\n early in the input list' % xform,
                               button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')

    # select each of the points from the list and create a cluster
    cmds.select(cl=True)
    for elem in elements:
        cmds.select(elem, add=True)

    # ---------------- put a control for this to be either relative or not (relative should NOT orient to surface if
    # you're going to parent)
    # ---------------- ORRRRR just keept the cluster around and drive it from the ws xforms of the controls

    # ---------------- BEST SOLUTION - keep the cluseter relative, group it, orient the ctrl, then parent group to control and then PARENT CONSTRAIN the cluster itself to the control

    clus = cmds.cluster(relative=False, name="{0}_CLS".format(ssDefName))

    for i in range(len(elements)):
        element = elements[i]
        value = weights[i]
        # percent -v 0.5 thisCluster pSphere1.vtx[241] ;
        cmds.percent(clus[0], element, v=value, )

    # get cluster position
    clusPos = cmds.xform(clus[1], ws=True, q=True, rp=True)

    cpomPos = avgElementPos(elements)

    if ssCPOM:
        cpomPos = rig.closest_pt_on_mesh_position(clus[1], mesh)

    cpomRot = rig.closest_pt_on_mesh_rotation(cpomPos, xform)

    control = rig.createControl(ssDefName, type="sphere", axis="x", color="blue")
    rig.scale_nurbs_control(control, ssScale)
    controlGrp = cmds.group(control, n="{0}_GRP".format(control))

    cmds.xform(controlGrp, ws=True, t=(cpomPos[0], cpomPos[1], cpomPos[2]))
    cmds.xform(controlGrp, ws=True, ro=(cpomRot[0], cpomRot[1], cpomRot[2]))

    clusHandShape = cmds.listRelatives(clus[1], s=True)

    cmds.cluster(clus[0], e=True, bindState=1, weightedNode=(control, control))

    cmds.setAttr("{0}.originX".format(clusHandShape[0], 0.0))
    cmds.setAttr("{0}.originY".format(clusHandShape[0], 0.0))
    cmds.setAttr("{0}.originZ".format(clusHandShape[0], 0.0))

    cmds.delete(clus[1])

    cmds.setAttr("{0}.visibility".format(clusHandShape[0]), 0)

# TODO - here do the same thing - textField for parent, if no parent, parent to worldSPace
    if ssParent:
        cmds.parent(controlGrp, xform)

    cmds.select(control, r=True)

    if ssIncrement == 1:
        newName = rig.increment_name(ssDefName)
        cmds.textFieldGrp(widgets["ssdTFG"], tx=newName, e=True)


# ------------------------
# helper functions
# ------------------------

def getDeformers(obj, *args):
    """gets a list of deformers on the passed obj"""
    history = cmds.listHistory(obj)
    deformerList = []
    for node in history:
        types = cmds.nodeType(node, inherited=True)
        if "geometryFilter" in types:
            deformerList.append(types[1])
    return deformerList


def avgElementPos(verts, *args):
    """uses a list of verts and gets the average position"""
    xVal = []
    yVal = []
    zVal = []
    xAll = 0.0
    yAll = 0.0
    zAll = 0.0

    for vert in verts:
        pos = cmds.pointPosition(vert)
        xVal.append(pos[0])
        yVal.append(pos[1])
        zVal.append(pos[2])

    for x in xVal:
        xAll += x
    for y in yVal:
        yAll += y
    for z in zVal:
        zAll += z

    avgX = xAll / len(xVal)
    avgY = yAll / len(yVal)
    avgZ = zAll / len(zVal)

    avgPos = (avgX, avgY, avgZ)

    return avgPos


#########
# joint stuff 
#########
def applyWeights(*args):
    vtxs, wts = get_soft_selection()
    tform = vtxs[0].partition(".")[0]
    mesh = cmds.listRelatives(tform, f=True, s=True)[0]

    ps = []
    center = []
    for vtx in vtxs:
        ps.append(cmds.pointPosition(vtx))
        center = [sum(y) / len(y) for y in zip(*ps)]

    # create joint at location
    # ----------- should get closest point on surface   
    cmds.select(cl=True)
    jnt = cmds.joint()
    cmds.xform(jnt, ws=True, t=center)

    # add influence to skin Cluster
    cmds.select(tform, r=True)
    cmds.skinCluster(e=True, ai=jnt, wt=0)

    # apply weights to that joint
    cls = mel.eval("findRelatedSkinCluster " + tform)
    for v in range(len(vtxs)):
        cmds.skinPercent(cls, vtxs[v], transformValue=[jnt, wts[v]])


def softDeformer():
    """Use this to start the script!"""
    softDeformerUI()
