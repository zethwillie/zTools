import maya.cmds as cmds
import zbw_rig as rig

crv = cmds.ls(sl=True)[0]

cvs = cmds.ls("%s.cv[*]"%crv, fl=True)
orList = []

for x in range(0, len(cvs)):
    cv = cvs[x]
    
    pos = cmds.pointPosition(cv)
    
    clsName = "%s_%s"%(crv, x)
    cls = cmds.cluster(cv, n=clsName)[1]
    ctrl = rig.createControl(name="%sCtrl"%clsName, type="sphere", color="red")
    grpOrient = rig.groupOrient(cls, ctrl)
    orList.append(grpOrient)
    cmds.parent(cls, ctrl)
    cmds.setAttr("%s.v"%cls, 0)

cmds.group(orList, n="crvCtrlsGrp")