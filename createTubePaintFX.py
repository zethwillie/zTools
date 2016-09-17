import maya.cmds as cmds

x = cmds.AttachBrushToCurves()
strokes = cmds.ls(type="stroke")
strkShp = strokes[-1]

brsh = cmds.listConnections(strkShp)[0]

#set brush stuff
cmds.setAttr("{}.globalScale".format(brsh), 1)
# hook!
cmds.setAttr("{}.brushWidth".format(brsh), 0.1)
cmds.setAttr("{}.twist".format(brsh), 1)
cmds.setAttr("{}.tubeSections".format(brsh), 12)


print thisBrush