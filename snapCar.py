import maya.cmds as cmds
"""
once you detach the car from the constraint it will snap back to god node.
with the carMasterCtrl still selected, run this [snapCar()] and it will put the free floating
car control right back on top of the car constrainer object (on that frame)
"""

def snapCar(*args):
    sel = cmds.ls(sl=True)

    if sel:
        ctrl = sel[0]
        attrs = cmds.listAttr(ctrl, ud=True)
        if "constrainer" in attrs:
            constr = cmds.listConnections("%s.constrainer"%ctrl)[0]
            
            posZOffset = -248.651424242
            pos = cmds.xform(constr, ws=True, q=True, rp=True)
            rot = cmds.xform(constr, ws=True, q=True, ro=True)
            
            cmds.xform(ctrl, ws=True, t=pos)
            cmds.xform(ctrl, ws=True, ro=rot)
            
            cmds.xform(ctrl, os=True, r=True, t=(0,0,posZOffset))
            
            
        else:
            cmds.warning("you haven't selected a carMasterCtrl")
    
    else:
        cmds.warning("You haven't selected a carMasterCtrl!")   
    