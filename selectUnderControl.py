import maya.cmds as cmds

sel = cmds.ls(sl=True)[0]

rels = cmds.listRelatives(sel, ad=True, type="nurbsCurve")

cmds.select(cl=True)
for rel in rels:
    parent = cmds.listRelatives(rel, p=True, type="transform")[0]
    cmds.select(parent, tgl=True)
    cmds.select(sel, tgl=True)