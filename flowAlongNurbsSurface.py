import maya.cmds as cmds


#verts = cmds.ls("pPlane3.vtx[*]", fl=True)
#cmds.select(cl=True)
#cVerts = []
#for x in range(1, len(verts), 3):
#    cVerts.append(verts[x])
    
#for vert in cVerts:
#    pos = cmds.pointPosition(vert)
#    
#    jnt = cmds.joint()
#    cmds.xform(jnt, ws=True, t=pos)
    
#num = len(cVerts)
#51

sel = cmds.ls(sl=True)
for x in range(len(sel)):
    mult = x * .004
    cmds.setAttr("%s.parameterV"%sel[x], mult)
#    print x, sel[x]

#sel = cmds.ls(sl=True)

#for x in range(len(sel)):
#    fol = "follicle%s"%(x+1)
#    jnt =sel[x]
#    
#    pos = cmds.xform(fol, ws= True, q=True, rp=True)
#    rot = cmds.xform(fol, ws=True, q=True, ro=True)
#    
#    cmds.xform(jnt, ws=True, t=pos)
#    cmds.xform(jnt, ws=True, ro=rot)
#    
#    cmds.parent(jnt, fol)


sel = cmds.ls(sl=True)

flow = "flowMult.outputX"

for fol in sel:
    v = cmds.getAttr("%s.parameterV"%fol)
    
    add = cmds.shadingNode("addDoubleLinear", n="%sAdd"%fol, asUtility=True)
    
    cmds.setAttr("%s.input2"%add, v)
    cmds.connectAttr(flow, "%s.input1"%add)
    cmds.connectAttr("%s.output"%add, "%s.parameterV"%fol)
    






