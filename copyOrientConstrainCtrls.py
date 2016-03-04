import maya.cmds as cmds

sel = cmds.ls(sl=True)

ctrl = sel[0]

for j in range(1, len(sel)):
    newName = "%sCtrl"%sel[j]
    grpName = "%sGrp"%newName   
   
    dCtrl = cmds.duplicate(ctrl)
    cmds.rename(dCtrl, newName)
    
    grp = cmds.group(em=True, n=grpName)
    cmds.parent(newName, grp)
    
    oc = cmds.orientConstraint(sel[j], grp)
    pc = cmds.pointConstraint(sel[j], grp)
    
    cmds.delete(oc, pc)
    
    cmds.parentConstraint(newName, sel[j])