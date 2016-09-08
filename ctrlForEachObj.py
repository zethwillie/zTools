"""one ctrl for each object selected, select ctrl first"""

import maya.cmds as cmds

sel = cmds.ls(sl=True)

origCtrl = sel[0]
cPos = cmds.xform(origCtrl, q=True, ws=True, rp=True)
cRot = cmds.xform(origCtrl, q=True, ws=True, ro=True)

for x in range(1, len(sel)):
    obj = sel[x]
    ctrl = cmds.duplicate(origCtrl, n="{}Ctrl".format(obj))
    grp = cmds.group(em=True, n="{}Grp".format(ctrl))
    cmds.xform(grp, ws=True, t=cPos)
    cmds.xform(grp, ws=True, ro=cRot)
        
    cmds.parent(ctrl, grp)
    
    pos = cmds.xform(obj, q=True, ws=True, rp=True)
    rot = cmds.xform(obj, q=True, ws=True, ro=True)
    
    cmds.xform(grp, ws=True, t=pos)
    cmds.xform(grp, ws=True, ro=rot)
    
    cmds.parent(obj, ctrl)