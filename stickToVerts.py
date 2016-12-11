import maya.cmds as cmds
import zTools.zbw_rig as rig
import zTool.mayaDecorators as md
reload(rig)

@md.d_showWaitCursor
def dupeToVert():
	sel = cmds.ls(sl=True, fl=True)
	instanceGrp = cmds.group(empty=True, name="instanceGrp")

	for v in sel:
		pos = cmds.pointPosition(v)
		obj = cmds.instance("pCylinder1")
		cmds.xform(obj, ws=True, t=pos)
		uv = rig.getVertUV([v])[0]
		folNum = v.partition(".")[2].partition("[")[2].strip("]")
		mesh = v.partition(".")[0]
		folName = "follicle_{0}".format(folNum)
		foll = rig.follicle(mesh, folName, u=uv[0], v=uv[1])
		cmds.parent(obj, foll)
		cmds.parent(foll, instanceGrp)

dupeToVert()