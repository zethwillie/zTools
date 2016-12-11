import maya.cmds as cmds

sel = cmds.ls(sl=True)[0]

cvs = cmds.ls("{}.cv[*]".format(sel), fl=True)

posList = []

for cv in cvs:
    pos = cmds.pointPosition(cv)
    posList.append(pos)
   
print posList