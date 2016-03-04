#scripts from dragon rig makin' at Buck

#create quick select set for selected controls

import maya.cmds as cmds

sel = cmds.ls(sl=True)

cmds.sets(text="gCharacterSet", name="headControls")

for obj in sel:
    cmds.sets("headControls", e=True, add=obj)


#apply a series of blend shapes to a series of objects

import maya.cmds as cmds

sel = cmds.ls(sl=True)

for x in range(0, len(sel)):
    num = (x%10)+1
    thisTarget = "lf_stripWaveDriver%02d_geo"%num

    BS = cmds.blendShape(thisTarget, sel[x], origin="local")
    cmds.blendShape(BS, e=True, w=[(0,1)])


#to create bend deformers on each of the driving cards and orient them correctly

import maya.cmds as cmds

sel = cmds.ls(sl=True)

for obj in sel:
    bend = cmds.nonLinear(obj, type="bend", lowBound=-2.1, highBound=0, curvature=0)
    bendHandle = "%s_bend"%obj
    cmds.rename(bend[1], bendHandle)

    cmds.xform(bendHandle, os=True, r=True, ro=(0,0,0))
    cmds.xform(bendHandle, os=True, r=True, t=(0,1,0))


#to replace side card geo with relatively shifted versions of the first one selected (so that can drive blend shapes)

import maya.cmds as cmds

#get all
sel = cmds.ls(sl=True)

#first is the base
base = sel[0]

#loop through the rest, get the pos of the card, dupe the bsae, move it to the pos and delete the orig card
for x in range(1, len(sel)):
    cardPos = cmds.xform(sel[x], q=True, ws=True, rp=True)

    newCard = cmds.duplicate(base, n="%s_1"%sel[x])

    cmds.xform(newCard, ws=True, t=cardPos)

    cmds.delete(sel[x])


#code to reorder the deformers so the scales happen (tweak, lattice)

sel = cmds.ls(sl=True)

baseAttr = "COG_CTRL.scalesPuffer"

for obj in sel:
    #get tweak deformer on obj
    shape = cmds.listRelatives(obj, s=True)
    tweak = cmds.listConnections(shape)[8] #here should use tweak = cmds.listConnections(shape, type="tweak")

    #print(tweak)
    #reorder two deformers
    cmds.reorderDeformers(tweak, "ffd1", obj)
    cmds.connectAttr(baseAttr, "%s.ry"%obj)

# to stick a group in btween (group orient after the fact)
import maya.cmds as cmds

objs = cmds.ls(sl=True)

for obj in objs:
    parent = cmds.listRelatives(obj, p=True)[0]
    rot = cmds.xform(obj, q=True, ws=True, ro=True)
    pos =cmds.xform(obj, q=True, ws=True, rp=True)

    grp = cmds.group(empty=True, n=(obj+"_GRP"))
    cmds.xform(grp, ws=True, ro=rot)
    cmds.xform(grp, ws=True, t=pos)
    cmds.parent(obj, grp)
    cmds.parent(grp, parent)

#to change the local rotational axis

import maya.cmds as cmds

sel = cmds.ls(sl=True)
for obj in sel:
    cmds.xform(obj, os=True, r=False, ra=(0, 180, 23.5))


#to put select objs' pivots onto the closest point on a mesh that sort of tracks where you want them to be

import maya.cmds as cmds
mesh = "polyShape"
cpom = cmds.shadingNode("closestPointOnMesh", n="cpom", asUtility=True)
cmds.connectAttr("%s.mesh"%mesh, "%s.inputSurface"%cpos)

objs = cmds.ls(sl=True)

for obj in objs:
    #get position
    objPos = cmds.xform(obj, q=True, ws=True, rp=True)
    cmds.setAttr("%s.inPosition"%cpom, objPos[0], objPos[1], objPos[2])

    #get position on surface
    pos = cmds.getAttr("%s.position"%cpom)

    #change pivot
    cmds.xform(obj, ws=True, piv=pos[0])

#to connect a vis attr to the vis of the shape nodes

import maya.cmds as cmds

sel = cmds.ls(sl=True)

for ctrl in sel:
    thisShape = cmds.listRelatives(ctrl, s=True, c=True)
    cmds.connectAttr("COG_CTRL.fineShaperCtrls", "%s.visibility"%thisShape[0])

#to add controls to selected cvs (via cluster, replace weighted node w/control)
import maya.cmds as cmds
import zbw_rig as rig

sel = cmds.ls(sl=True, fl=True)

for i in range(len(sel)):
    #create a cluster
    cluster = cmds.cluster(sel[i], relative=False, n="cluster%02d"%i)
    #print(cluster)
    #for that cluster, create a circle control at that cluster
    ctrl = rig.createControl("control%02d"%i, "sphere", "z", "blue")
    rig.groupOrient(cluster[1], ctrl)
    #replace the weighted node of the cluster with the circle
    clusHandShape = cmds.listRelatives(cluster[1], s=True)
    cmds.cluster(cluster[0], e=True, bs=1, wn=(ctrl, ctrl))

    cmds.setAttr("%s.originX"%clusHandShape[0], 0.0)
    cmds.setAttr("%s.originY"%clusHandShape[0], 0.0)
    cmds.setAttr("%s.originZ"%clusHandShape[0], 0.0)
    cmds.setAttr("%s.visibility"%clusHandShape[0], 0)