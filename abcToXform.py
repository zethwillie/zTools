import maya.cmds as cmds

sel = cmds.ls(sl=True)
 
for abc in sel:
	shps = [x for x in cmds.listRelatives(abc, s=True)]
	pos = cmds.xform(abc, ws=True, q=True, rp=True)
	par = ""
	parList = cmds.listRelatives(abc, p=True)
	if parList:
		par = parList[0]
	for shp in shps:
		nShp=cmds.rename(shp, "{0}Shape".format(shp))
		xf = cmds.group(em=True, name=shp)
		cmds.xform(xf, ws=True, t=pos)
		cmds.parent(nShp, xf, r=True, s=True)
		if par:
			cmds.parent(xf, par)
		# delete rotation? 
	cmds.delete(abc)

____________________

import maya.cmds as cmds

sel = cmds.ls(sl=True)
cam = sel[0]
objs = sel[1:]

camPos = cmds.xform(cam, ws=True, q=True, rp=True)

for obj in objs:
	cmds.xform(obj, ws=True, piv=camPos)	
	cmds.setAttr("{0}.rx".format(obj), 0)
	cmds.setAttr("{0}.ry".format(obj), 0)
	cmds.setAttr("{0}.rz".format(obj), 0)