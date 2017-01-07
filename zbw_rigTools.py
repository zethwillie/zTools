#zbw_rigTools

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

########
import zTools.zbw_rig as rig
from functools import partial

########## -------- add some tooltips to these buttons

widgets = {}

zDict = {"attr":"import zTools.zbw_attributes as zat; zat.attributes()", 
"snap":"import zTools.zbw_snap as snap; snap.snap()",
"shpScl":"import zTools.zbw_shapeScale as zss; zss.shapeScale()",
"selBuf":"import zTools.selectionBuffer as buf; buf.selectionBuffer()",
"smIK":"import zTools.zbw_smallIKStretch as zsik; zsik.smallIKStretch()",
"foll":"import zTools.zbw_makeFollicle as zmf; zmf.makeFollicle()",
"ribbon":"import zTools.zbw_ribbon as zrib; zrib.ribbon()",
"soft":"import zTools.zbw_softDeformer as zsft; zsft.softDeformer()",
"jntRadius":"import zTools.zbw_jointRadius as jntR; jntR.jointRadius()", 
"randSelect":"import zTools.zbw_randomSelection as zrand; reload(zrand); zrand.randomSelection()",
"trfmBuffer":"import zTools.zbw_transformBuffer as ztbuf; reload(ztbuf); ztbuf.transformBuffer()", 
"crvTools":"import zTools.zbw_curveTools as ctool; reload(ctool); ctool.curveTools()", 
"rndAttr":"import zTools.zbw_randomAttrs as rndat; reload(rndat); rndat.randomAttrs()", 
"extrRig":"import zTools.curveExtrudeRig as extr; reload(extr); extr.curveExtrude()"
}

colors = {'red':13, 'blue':6, 'green':14, 'yellow':17, 'pink':20, 'ltBlue':18, 'brown':10, 'purple':30, 'dkGreen':7}


def rigToolsUI(*args):
    if cmds.window("rigToolWin", exists=True):
        cmds.deleteUI("rigToolWin")

    widgets["win"] = cmds.window("rigToolWin", t="zbw_rigTools", w=280, rtf=True, s=False)
    widgets["mainCLO"] = cmds.columnLayout(w=280, h=570)
    widgets["mainFLO"] = cmds.formLayout(w=280, h=610, bgc = (0.1,0.1,0.1))

#controls layout
    widgets["ctrlFLO"] = cmds.formLayout(w=110, h=380, bgc = (0.3,0.3,0.3))
    widgets["ctrlFrLO"] = cmds.frameLayout(l="CONTROLS", w=110, h=380, bv=True, bgc = (0.3,0.3,0.3))
    widgets["ctrlCLO"] = cmds.columnLayout(bgc = (0.3,0.3,0.3))

    widgets["circleBut"] = cmds.button(l="circle", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "circle"))
    widgets["sphereBut"] = cmds.button(l="sphere", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "sphere"))
    widgets["squareBut"] = cmds.button(l="square", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "square"))
    widgets["boxBut"] = cmds.button(l="box", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "box"))
    widgets["lolBut"] = cmds.button(l="lollipop", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "lollipop"))
    widgets["barbellBut"] = cmds.button(l="barbell", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "barbell"))
    widgets["crossBut"] = cmds.button(l="cross", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "cross"))
    widgets["bentXBut"] = cmds.button(l="bent cross", h=20, w=110, bgc=(.7, .7, .5), c = partial(control, "bentCross"))
    widgets["arrowBut"] = cmds.button(l="arrow", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "arrow"))
    widgets["bentArrowBut"] = cmds.button(l="bent arrow", h=20, w=110, bgc=(.7, .7, .5), c = partial(control, "bentArrow"))
    widgets["splitOBut"] = cmds.button(l="split circle", h=20, w=110, bgc=(.7, .7, .5), c = partial(control, "splitCircle"))
    widgets["cylinderBut"] = cmds.button(l="cylinder", h=20, w=110, bgc=(.7, .7, .5), c = partial(control, "cylinder"))
    widgets["starBut"] = cmds.button(l="star", w=110, h=20, bgc=(.7, .7, .5), c = partial(control, "star"))
    widgets["octagonBut"] = cmds.button(l="octagon", h=20, w=110, bgc=(.7, .7, .5), c = partial(control, "octagon"))
    widgets["halfCircBut"] = cmds.button(l="half circle", h=20, w=110, bgc=(.7, .7, .5), c = partial(control, "halfCircle"))
    widgets["crossArrow"] = cmds.button(l="arrow cross", h=20, w=110, bgc=(.7, .7, .5), c = partial(control, "arrowCross"))	
    cmds.separator(h=10, style="none")
    widgets["ctrlAxisRBG"] = cmds.radioButtonGrp(nrb=3, la3=("x", "y", "z"), cw=([1, 33], [2, 33], [3, 33]), cal=([1, "left"], [2, "left"], [3, "left"]), sl=1)

#action layout
    cmds.setParent(widgets["mainFLO"])
    widgets["actionFLO"] = cmds.formLayout(w=150, h=288, bgc = (0.3,0.3,0.3))
    widgets["actionFrLO"] = cmds.frameLayout(l="ACTIONS", w=150, h=288, bv=True, bgc = (0.3,0.3,0.3))
    widgets["actionCLO"] = cmds.columnLayout(bgc = (0.3,0.3,0.3))
    widgets["grpFrzBut"] = cmds.button(l="group freeze selected", w=150, bgc=(.5, .7, .5), c = groupFreeze)
    widgets["grpAbvBut"] = cmds.button(l="insert group above ('Grp')", w=150, bgc=(.5, .7, .5), c = insertGroupAbove)
    widgets["grpCnctBut"] = cmds.button(l="group freeze connect", w=150, bgc=(.5, .7, .5), c = freezeAndConnect)
    widgets["slctHiBut"] = cmds.button(l="select hierarchy", w=150, bgc=(.5, .7, .5), c = selectHi)	
    widgets["prntChnBut"] = cmds.button(l="parent chain selected", w=150, bgc=(.5, .7, .5), c = parentChain)
    widgets["hideShp"] = cmds.button(l="selection toggle shape vis", w=150, bgc=(.5, .7, .5), c=hideShape)	
    widgets["slctCmptBut"] = cmds.button(l="select components", w=150, bgc=(.5, .7, .5), c = selectComponents)
    widgets["bBox"] = cmds.button(l="bounding box control", w=150, bgc=(.5, .7, .5), c=bBox)	
    widgets["cpSkinWtsBut"] = cmds.button(l="copy skin & weights", w=150, bgc=(.5, .7, .5), c = copySkinning)	
    widgets["remNSBut"] = cmds.button(l="remove all namespaces", w=150, bgc=(.5, .7, .5), c = remNS)	
    widgets["cntrLoc"] = cmds.button(l="selection center locator", w=150, bgc=(.5, .7, .5), c = centerLoc)

#zScript Layout
    cmds.setParent(widgets["mainFLO"])
    widgets["zScrptFLO"] = cmds.formLayout(w=280, h=270, bgc = (0.3,0.3,0.3))
    widgets["zScrptFrLO"] = cmds.frameLayout(l="Z_SCRIPTS", w=280, h=270, bv=True, bgc = (0.3,0.3,0.3))
    cmds.setParent(widgets["zScrptFLO"])	
    widgets["attrBut"] = cmds.button(l="zbw_attrs", w=135, bgc = (.7, .5, .5), c=partial(zAction, "attr"))
    widgets["shpSclBut"] = cmds.button(l="zbw_shapeScale", w=135, bgc = (.7, .5, .5), c=partial(zAction, "shpScl"))
    widgets["selBufBut"] = cmds.button(l="zbw_selectionBuffer", w=135, bgc = (.7, .5, .5), c=partial(zAction, "selBuf"))
    widgets["snapBut"] = cmds.button(l="zbw_snap", w=135, bgc = (.7, .5, .5), c=partial(zAction, "snap"))
    widgets["smIKBut"] = cmds.button(l="zbw_smallIKStretch", w=135, bgc = (.7, .5, .5), c=partial(zAction, "smIK"))
    widgets["sftDefBut"] = cmds.button(l="zbw_softDeformers", w=135, bgc = (.7, .5, .5), c=partial(zAction, "soft"))
    widgets["follBut"] = cmds.button(l="zbw_makeFollicle", w=135, bgc = (.7, .5, .5), c=partial(zAction, "foll"))
    widgets["ribbonBut"] = cmds.button(l="zbw_ribbon", w=135, bgc = (.7, .5, .5), c=partial(zAction, "ribbon"))
    widgets["jntRadBut"] = cmds.button(l="zbw_jointRadius", w=135, bgc = (.7, .5, .5), c=partial(zAction, "jntRadius"))
    widgets["randSelect"] = cmds.button(l="zbw_randomSelection", w=135, bgc = (.7, .5, .5), c=partial(zAction, "randSelect"))
    widgets["trnBuffer"] = cmds.button(l="zbw_transformBuffer", w=135, bgc = (.7, .5, .5), c=partial(zAction, "trfmBuffer"))	
    widgets["crvTools"] = cmds.button(l="zbw_randomAttrs", w=135, bgc = (.7, .5, .5), c=partial(zAction, "rndAttr"))
    widgets["rndAttr"] = cmds.button(l="zbw_curveTools", w=135, bgc = (.7, .5, .5), c=partial(zAction, "crvTools"))	
    widgets["extrRig"] = cmds.button(l="curveExtrudeRig", w=135, bgc = (.7, .5, .5), c=partial(zAction, "extrRig"))	

#color layout
    cmds.setParent(widgets["mainFLO"])
    widgets["colorFLO"] = cmds.formLayout(w=150, h=88, bgc = (0.3,0.3,0.3))
    widgets["colorFrLO"] = cmds.frameLayout(l="COLORS", w=150, h=88, bv=True, bgc = (0.3,0.3,0.3))
    widgets["colorRCLO"] = cmds.rowColumnLayout(nc=3)
    #cmds.setParent(widgets["colorFLO"])

    widgets["redCNV"] = cmds.canvas(w=50, h=20, rgb=(1,0,0), pc=partial(changeColor, colors["red"]))
    widgets["blueCNV"] = cmds.canvas(w=50, h=20, rgb=(0,0,1), pc=partial(changeColor, colors["blue"]))
    widgets["greenCNV"] = cmds.canvas(w=50, h=20, rgb=(0,1,0), pc=partial(changeColor, colors["green"]))
    widgets["yellowCNV"] = cmds.canvas(w=50, h=20, rgb=(1,1,0), pc=partial(changeColor, colors["yellow"]))
    widgets["pinkCNV"] = cmds.canvas(w=50, h=20, rgb=(1,.8,.965), pc=partial(changeColor, colors["pink"]))
    widgets["ltBlueCNV"] = cmds.canvas(w=50, h=20, rgb=(.65,.8,1), pc=partial(changeColor, colors["ltBlue"]))
    widgets["brownCNV"] = cmds.canvas(w=50, h=20, rgb=(.5,.275,0), pc=partial(changeColor, colors["brown"]))
    widgets["purpleCNV"] = cmds.canvas(w=50, h=20, rgb=(.33,0,.33), pc=partial(changeColor, colors["purple"]))
    widgets["dkGreenCNV"] = cmds.canvas(w=50, h=20, rgb=(0,.35,0), pc=partial(changeColor, colors["dkGreen"]))

#formlayout stuff
    cmds.formLayout(widgets["mainFLO"], e=True, af=[
        (widgets["ctrlFLO"], "left", 0),
        (widgets["ctrlFLO"], "top", 0), 
        (widgets["actionFLO"], "left", 125),
        (widgets["actionFLO"], "top", 0),
        (widgets["zScrptFLO"], "left", 0),
        (widgets["zScrptFLO"], "top", 385),
        (widgets["colorFLO"], "left", 125),
        (widgets["colorFLO"], "top", 292),				
        ])

    cmds.formLayout(widgets["zScrptFLO"], e=True, af = [
        (widgets["attrBut"], "left", 0),
        (widgets["attrBut"], "top", 25),
        (widgets["selBufBut"], "left", 140),
        (widgets["selBufBut"], "top", 25),
        (widgets["shpSclBut"], "left", 0),
        (widgets["shpSclBut"], "top", 50),
        (widgets["snapBut"], "left", 140),
        (widgets["snapBut"], "top", 50),
        (widgets["smIKBut"], "left", 0),
        (widgets["smIKBut"], "top", 75),
        (widgets["sftDefBut"], "left", 140),
        (widgets["sftDefBut"], "top", 75),
        (widgets["follBut"], "left", 0),
        (widgets["follBut"], "top", 100),
        (widgets["ribbonBut"], "left", 140),
        (widgets["ribbonBut"], "top", 100),	
        (widgets["jntRadBut"], "left", 0),
        (widgets["jntRadBut"], "top", 125),
        (widgets["randSelect"], "left", 140),
        (widgets["randSelect"], "top", 125),
        (widgets["trnBuffer"], "left", 0),
        (widgets["trnBuffer"], "top", 150),						
        (widgets["rndAttr"], "left", 140),
        (widgets["rndAttr"], "top", 150),			
        (widgets["crvTools"], "left", 0),
        (widgets["crvTools"], "top", 175),	
        (widgets["extrRig"], "left", 140),
        (widgets["extrRig"], "top", 175),			
        ])	
    
    cmds.window(widgets["win"], e=True, rtf=True, w=5, h=5)
    cmds.showWindow(widgets["win"])

##########
# functions
##########

def control(type="none", *args):
    """gets teh name from the button pushed and the axis from the radio button group"""
    axisRaw = cmds.radioButtonGrp(widgets["ctrlAxisRBG"], q=True, sl=True)
    if axisRaw == 1:
        axis = "x"
    if axisRaw == 2:
        axis = "y"
    if axisRaw == 3:
        axis = "z"				

    rig.createControl(name = "Ctrl", type = type, axis = axis, color = "yellow")

def zAction(action="none", *args):
    """grabs the action key from the dictionary and executes that value"""
    
    if action != "none":
        x = zDict[action]
        print "executing: {}".format(x)
        exec(x)

    else:
        cmds.warning("zbw_rigTools.zAction: For some reason this script isn't in my dictionary")

def remNS(*args):
    """removes namespaces . . . """

    rem = ["UI", "shared"]
    ns = cmds.namespaceInfo(lon=True, r=True)
    for y in rem:
        ns.remove(y)

    ns.sort(key = lambda a: a.count(":"), reverse=True)
    for n in ns:
        ps = cmds.ls("{}:*".format(n), type="transform")
        for p in ps:
            cmds.rename(p, p.rpartition(":")[2]) 
        cmds.namespace(rm=n)

def groupFreeze(*args):
    """group freeze an obj"""

    sel = cmds.ls(sl=True)

    for obj in sel:
        pos = cmds.xform(obj, q=True, ws=True, rp=True)
        rot = cmds.xform(obj, q=True, ws=True, ro=True)
        scl = cmds.xform(obj, q=True, r=True, s=True)
        grp = cmds.group(em=True, n="{}Grp".format(obj))
        cmds.xform(grp, ws=True, t=pos)
        cmds.xform(grp, ws=True, ro=rot)
        cmds.xform(grp, s=scl)
        
        cmds.parent(obj, grp)
        cmds.select(grp, r=True)


def nameCheck(name):
    if cmds.objExists(name):
        name = "{}_GRP".format(name)
        print name
        nameCheck(name)
    else:
        return(name)

def insertGroupAbove(*args):
    sel = cmds.ls(sl=True)

    for obj in sel:
        par = cmds.listRelatives(obj, p=True)
        
        grp = cmds.group(em=True, n="{}_Grp".format(obj))
        
        # grp = nameCheck(grp)

        pos = cmds.xform(obj, q=True, ws=True, rp=True)
        rot = cmds.xform(obj, q=True, ws=True, ro=True)
        
        cmds.xform(grp, ws=True, t=pos)
        cmds.xform(grp, ws=True, ro=rot) 
         
        cmds.parent(obj, grp)
        if par:
            cmds.parent(grp, par[0])


def freezeAndConnect(*args):
    sel = cmds.ls(sl=True)

    ctrlOrig = sel[0]

    for x in range(1, len(sel)):
        obj = sel[x]
        ctrl = cmds.duplicate(ctrlOrig, n = "{}Ctrl".format(obj))[0]
        
        pos = cmds.xform(obj, ws=True, q=True, rp=True)
        rot = cmds.xform(obj, ws=True, q=True, ro=True)
        
        grp = cmds.group(em=True, n="{}Grp".format(ctrl))
        
        cmds.parent(ctrl, grp)
        cmds.xform(grp, ws=True, t=pos)
        cmds.xform(grp, ws=True, ro=rot)
        
        cmds.parentConstraint(ctrl, obj)

def parentChain(*args):
    #parent chain (select objs, child first. WIll parent in order selected)

    sel = cmds.ls(sl=True)
    sizeSel = len(sel)
    for x in range(0, sizeSel-1):
        cmds.parent(sel[x], sel[x+1])

def selectHi(*args):
    cmds.select(hi=True)

def selectComponents(*args):
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

def controlsOnCurve(*args):
    pass

def changeColor(color, *args):
    """change shape color of selected objs"""

    sel = cmds.ls(sl=True)

    if sel:
        for obj in sel:
            shapes = cmds.listRelatives(obj, s=True)
            if shapes:
                for shape in shapes:
                    cmds.setAttr("%s.overrideEnabled"%shape, 1)
                    cmds.setAttr("%s.overrideColor"%shape, color)


def copySkinning(*args):
    """select the orig bound mesh, then the new unbound target mesh and run"""

    sel = cmds.ls(sl=True)
    orig = sel[0]
    target = sel[1]

    #get orig obj joints
    try:
        jnts = cmds.skinCluster(orig, q=True, influence = True)
    except:
        cmds.warning("couldn't get skin weights from {}".format(orig))

    #bind the target with the jnts
    try:
        targetClus = cmds.skinCluster(jnts, target, bindMethod=0, skinMethod=0, normalizeWeights=1, maximumInfluences = 3, obeyMaxInfluences=False, tsb=True)[0]
        print targetClus
    except:
        cmds.warning("couln't bind to {}".format(target))
            
    #get skin clusters
    origClus = mel.eval("findRelatedSkinCluster " + orig)

    #copy skin weights from orig to target
    try:
        cmds.copySkinWeights(ss=origClus, ds=targetClus, noMirror=True, sa="closestPoint", ia="closestJoint")
    except:
        cmds.warning("couldn't copy skin weights from {0} to {1}".format(orig, target))


def centerLoc(*args):
    """creates a center loc on the avg position"""

    sel = cmds.ls(sl=True, fl=True)
    if sel:
        ps = []
        for vtx in sel:
            ps.append(cmds.xform(vtx, q=True, ws=True, rp=True))

        # this is cool!
        center = [sum(y)/len(y) for y in zip(*ps)]

        loc = cmds.spaceLocator(name="centerLoc")
        cmds.xform(loc, ws=True, t=center)

def hideShape(*args):
    """hides the shape nodes of the selected objects"""

    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            shp = cmds.listRelatives(obj, shapes = True)
            if shp:
                for s in shp:
                    if cmds.getAttr("{}.visibility".format(s)):
                        cmds.setAttr("{}.visibility".format(s), 0)
                    else:
                        cmds.setAttr("{}.visibility".format(s), 1)

def bBox(*args):
    """creates a control based on the bounding box"""
    sel = cmds.ls(sl=True)

    box = cmds.exactWorldBoundingBox(sel) #[xmin, ymin, zmin, xmax, ymax, zmax]
    X = om.MVector(box[0], box[3])
    Y = om.MVector(box[1], box[4])
    Z = om.MVector(box[2], box[5])

    #get bbox lengths along axes
    lenX = (X.y - X.x)
    lenY = (Y.y - Y.x)
    lenZ = (Z.y - Z.x)

    print lenX, lenY, lenZ

    ctrl = rig.createControl(name="ctrl", type="cube", color="pink")

    cvs ={"xyz":[5, 15],"-xyz":[0, 4],"xy-z":[10, 14],"x-yz":[6, 8],"-x-yz":[3, 7],"-x-y-z":[2, 12],"x-y-z":[9, 13],"-xy-z":[1, 11]}

    for a in cvs["xyz"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.y, Y.y, Z.y))
    for a in cvs["-xyz"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.x, Y.y, Z.y))
    for a in cvs["x-yz"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.y, Y.x, Z.y))
    for a in cvs["-x-yz"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.x, Y.x, Z.y))
    for a in cvs["xy-z"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.y, Y.y, Z.x))
    for a in cvs["-xy-z"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.x, Y.y, Z.x))
    for a in cvs["-x-y-z"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.x, Y.x, Z.x))
    for a in cvs["x-y-z"]:
        cmds.xform("{0}.cv[{1}]".format(ctrl, a), ws=True, t=(X.y, Y.x, Z.x))
    
    # center pivot on ctrl
    cmds.xform(ctrl, cp=True)
    cmds.select(ctrl)
    return(ctrl)

##########
# load function
##########

def rigTools(*args):
    rigToolsUI()