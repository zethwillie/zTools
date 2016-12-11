import maya.cmds as cmds

#create locs
locList = [["ankleLoc",(0, 4, 0)], ["ballLoc", (0, 1, 3)], ["toeLoc", (0, 0, 7)], ["heelLoc", (0, 0, -2)]]

for loc in locList:
    thisLoc = cmds.spaceLocator(n=loc[0])
    cmds.xform(thisLoc, ws=True, t=loc[1])

ballPos = cmds.xform("ballLoc", q=True, ws=True, rp=True)
toePos = cmds.xform("toeLoc", q=True, ws=True, rp=True)
heelPos = cmds.xform("heelLoc", q=True, ws=True, rp=True)
anklePos = cmds.xform("ankleLoc", q=True, ws=True, rp=True)

ballGrp = cmds.group(em=True, n="ballPivot")
toeGrp = cmds.group(em=True, n="toePivot")
heelGrp = cmds.group(em=True, n="heelPivot")
ankleGrp = cmds.group(em=True, n="anklePivot")

cmds.xform(ballGrp, ws=True, t=ballPos)
cmds.xform(toeGrp, ws=True, t=toePos)
cmds.xform(heelGrp, ws=True, t=heelPos)
cmds.xform(ankleGrp, ws=True, t=anklePos)

cmds.parent("ballLoc", ballGrp)
cmds.parent(ballGrp, "toeLoc", toeGrp)
cmds.parent(toeGrp, "heelLoc", heelGrp)
cmds.parent(heelGrp, "ankleLoc", ankleGrp)
