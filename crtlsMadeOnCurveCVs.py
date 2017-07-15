import maya.cmds as cmds
import zTools.zbw_rig as rig


def controlsOnCurves(crv, *args):
		if not rig.isType(crv, "nurbsCurve"):
			return()
		
		cvs = cmds.ls("{0}.cv[*]".format(crv), fl=True)
		
		for x in range(0, len(cvs)):
			pos = cmds.pointPosition(cvs[x])
			shp = cmds.listRelatives(crv, s=True)[0]
			ctrl = rig.createControl(type="sphere", name="{0}_{1}_CTRL".format(crv, x), color="red")
			grp = rig.groupFreeze(ctrl)
			
			cmds.xform(grp, ws=True, t=pos)
			
			dm = cmds.shadingNode("decomposeMatrix", asUtility=True,name="{0}_{1}_DM".format(crv, x))
			cmds.connectAttr("{0}.worldMatrix[0]".format(ctrl), "{0}.inputMatrix".format(dm))
			cmds.connectAttr("{0}.outputTranslate".format(dm), "{0}.controlPoints[{1}]".format(shp, x))

crvs = cmds.ls(sl=True)
for crv in crvs:
	controlsOnCurves(crv)
	
