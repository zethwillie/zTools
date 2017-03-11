#TO-DO----------------also think about selecting all the cards. . . for each, run closestPointOnSurface function for the dummy geo, create a follicle at the closest point(UV) and parent it to that. . . .
import maya.cmds as cmds
import zbw_rig as rig

#TO-DO----------------maybe script breaking a poly shell into faces then attach those to the proxy geo

def cardAttach():
	sel = cmds.ls(sl=True)
	#get all the cards (could be groups)
	cards = sel[1:]

	#get the proxy geo
	shell = sel[0]

	#for each card (or group) get the nearest point on surface of proxy
	for card in cards:
		#use closest point on surface to get the uv
		cardPos = cmds.xform(card, ws=True, q=True, rp=True)
		cpom = cmds.shadingNode("closestPointOnMesh", asUtility=True, n="tempCPOM")
		cmds.connectAttr("%s.outMesh"%shell, "%s.inMesh"%cpom)
		cmds.setAttr("%s.inPosition"%cpom, cardPos[0], cardPos[1], cardPos[2])
		cmds.connectAttr("%s.worldMatrix"%shell, "%s.inputMatrix"%cpom)

		u = cmds.getAttr("%s.u"%cpom)
		v = cmds.getAttr("%s.v"%cpom)
		#from that uv, create a follicle on the proxy
		follicle = rig.follicle(shell, "%s_fol"%card, u=u, v=v)

		#constrain or parent the card to the follicle
		cmds.makeIdentity(apply=True, s=True)
		#cmds.parentConstraint(follicle[0], card, mo=True)

		cmds.parent(card, follicle[0])

		#delete the closestPoint on mesh
		cmds.delete(cpom)
