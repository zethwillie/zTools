"""one ctrl for all objects selected, select ctrl first"""

import maya.cmds as cmds

sel = cmds.ls(sl=True)

origCtrl = "ctrl"
print origCtrl
cPos = cmds.xform(origCtrl, q=True, ws=True, rp=True)
cRot = cmds.xform(origCtrl, q=True, ws=True, ro=True)
ctrl = cmds.duplicate(origCtrl, n="{}Ctrl".format(obj))[0]
#grp = cmds.group(em=True, n="{}Grp".format(ctrl))
#cmds.xform(grp, ws=True, t=cPos)
#cmds.xform(grp, ws=True, ro=cRot)
    
#cmds.parent(ctrl, grp)
objPosList = []
objRotList = []

for x in range(0, len(sel)):
    obj = sel[x]    
    pos = cmds.xform(obj, q=True, ws=True, rp=True)
    rot = cmds.xform(obj, q=True, ws=True, ro=True)
    objPosList.append(pos)
    objRotList.append(rot)
    
#xPosList = [x[0] for x in objPosList]
#yPosList = [x[1] for x in objPosList]
#zPosList = [x[2] for x in objPosList]

#xRotList = [x[0] for x in objRotList]
#yRotList = [x[1] for x in objRotList]
#zRotList = [x[2] for x in objRotList]

avgXpos = sum([x[0] for x in objPosList])/len(xPosList)
avgYpos = sum([x[1] for x in objPosList])/len(yPosList)
avgZpos = sum([x[2] for x in objPosList])/len(zPosList)

avgXrot = sum([x[0] for x in objRotList])/len(xRotList)
avgYrot = sum([x[1] for x in objRotList])/len(yRotList)
avgZrot = sum([x[2] for x in objRotList])/len(zRotList)

avgPos = (avgXpos, avgYpos, avgZpos)
avgRot  = (avgXrot, avgYrot, avgZrot)

objGrp = cmds.group(em=True, n="{}Grp".format(sel[1]))
cmds.xform(objGrp, ws=True, t=avgPos)
cmds.xform(objGrp, ws=True, ro=avgRot)
cmds.xform(objGrp, cp=True)

cmds.parent(sel, objGrp)

cmds.xform(ctrl, ws=True, t=avgPos)
cmds.xform(ctrl, ws=True, ro=avgRot)

cmds.parent(objGrp, ctrl)
    