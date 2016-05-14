import maya.cmds as cmds
import maya.OpenMaya as om

sel = cmds.ls(sl=True)

shldr = sel[0]
elbow = sel[1]
wrist = sel[2]

pvGrp = sel[3]

shldrPos = cmds.xform(shldr, q=True, ws=True, rp=True)
shldrVec = om.MVector(shldrPos[0], shldrPos[1], shldrPos[2])

elbowPos = cmds.xform(elbow, q=True, ws=True, rp=True)
elbowVec = om.MVector(elbowPos[0], elbowPos[1], elbowPos[2])

wristPos = cmds.xform(wrist, q=True, ws=True, rp=True)
wristVec = om.MVector(wristPos[0], wristPos[1], wristPos[2])

shldrWrist = (wristVec+shldrVec)*0.5
dir = elbowVec - shldrWrist
length = dir*10

pvPos = length + shldrWrist

cmds.xform("locator1", ws=True, t=pvPos)

#midElbowDif = elbowVec-shldrWristMid
#cmds.xform("locator1", ws=True, t=midElbow)