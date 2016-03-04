import maya.cmds as cmds
import zbw_rig as rig

"""
creates an fk control chain on selected joints (in order). select control reference object (to be copied) and then object to receive controls, then run. 
"""

#get ctrl
ctrl = cmds.ls(sl=True)[0]

#get each jnt
jnts = cmds.ls(sl=True)[1:]
grps= []
cldrn = []
#grp orient ctrl for each jnt
#get jnt name
for jnt in jnts:
    
    #duplicate control and rename, then group orient
    thisCtrl = cmds.duplicate(ctrl, name=jnt.rstrip("_JNT") + "_CTRL")[0]
    
    thisGrp = cmds.group(n=thisCtrl+ "_GRP", em=True)
    cmds.parent(thisCtrl, thisGrp)
    
    trans = cmds.xform(jnt, q=True, ws = True, rp = True)
    rot  = cmds.xform(jnt, q=True, ws = True, ro=True)
    
    #cmds.xform(thisGrp,ws=True, s = (1,-1,0))
    cmds.xform(thisGrp, ws=True, t = trans)
    cmds.xform(thisGrp, ws=True, ro = rot)
    cmds.parentConstraint(thisCtrl, jnt, mo=True)
    
    grps.append(thisGrp)
    cldrn.append(thisCtrl)
    
for x in range(len(grps)-1, 0, -1):
    cmds.parent(grps[x], cldrn[x-1])
    #print x, x-1
    

   