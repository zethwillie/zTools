#insert group below (based on location/orientation of selected

import maya.cmds as cmds

sel = cmds.ls(sl=True)

for obj in sel:
    pos = cmds.xform(obj, ws=True, q=True, rp=True)
    rot = cmds.xform(obj, ws=True, q=True, ro=True)
    
    children = cmds.listRelatives(obj, children=True)
    
    grp = cmds.group(em=True, name=obj.replace("Auto", "Manual"))
    
    cmds.xform(grp, ws=True, t=pos)
    cmds.xform(grp, ws=True, ro=rot)
    
    cmds.parent(grp, obj)
    for child in children:
        cmds.parent(child, grp) 
    

