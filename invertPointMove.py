import maya.cmds as cmds
"""moves points to undo tranform rotation and translation. select the object with the tranforms, then the zeroed out object. 
This will move the points of the latter to counter the translations of the former"""


def moveVerts(*args):
    sel = cmds.ls(sl=True)
    loc = sel[0]
    #get tranforms (rot, pos) of the original
    pos = cmds.xform(loc, q=True, ws=True, rp=True)
    rot = cmds.xform(loc, q=True, ws=True, ro=True)
    
    #select all vtx of the zeroed obj and moves them counter
    obj = sel[1]
    pts = cmds.select("%s.vtx[*]"%obj) 
    cmds.move(-pos[0], -pos[1], -pos[2], r=True, ws=True)
    cmds.rotate(-rot[0], -rot[1], -rot[2], r=True, ws=True)