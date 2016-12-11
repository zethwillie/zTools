import maya.cmds as cmds

sel = cmds.ls(sl=True)
shd = sel[0]
ctrls = sel[1:]

sg = cmds.listConnections(shd, type="shadingEngine")[0]

tNode = cmds.shadingNode("file", asTexture=True, name="fileTemplate", isColorManaged=True)
pNode = cmds.shadingNode("place2dTexture", asUtility=True, name="placeTemplate")
pAttrs = ["coverage", "translateFrame", "rotateFrame", "mirrorU", "mirrorV", "stagger", "wrapU", "wrapV", "repeatUV", "offset", "rotateUV", "noiseUV", "vertexUvOne", "vertexUvTwo", "vertexUvThree", "vertexCameraOne", "outUV", "outUvFilterSize"]
tAttrs = ["coverage", "translateFrame", "rotateFrame", "mirrorU", "mirrorV", "stagger", "wrapU", "wrapV", "repeatUV", "offset", "rotateUV", "noiseUV", "vertexUvOne", "vertexUvTwo", "vertexUvThree", "vertexCameraOne", "uv", "uvFilterSize"]

ts = cmds.shadingNode("tripleShadingSwitch", asUtility=True, name="{}_TripleSwitch".format(shd))
# may want to check here re: what input channel we want to use
cmds.connectAttr("{}.output".format(ts), "{}.color".format(shd))

for x in range(len(pAttrs)):
	cmds.connectAttr("{0}.{1}".format(pNode, pAttrs[x]), "{0}.{1}".format(tNode, tAttrs[x]))

for i in range(len(ctrls)):
	geo = cmds.connectionInfo("{}.geo".format(ctrls[i]), sfd=True).partition(".")[0]
	
	cmds.sets(geo, e=True, forceElement=sg)

	dupeNodes = cmds.duplicate(tNode, un=True, rc=True)
	fileNode = cmds.rename(dupeNodes[0], "{}_fileText".format(ctrls[i]))
	placeNode = cmds.rename(dupeNodes[1], "{}_place2d".format(ctrls[i]))
	cmds.connectAttr("{}.rptHolder".format(ctrls[i]), "{}.repeatUV.repeatV".format(placeNode))
	
	geoShp = cmds.listRelatives(geo, s=True)[0]
	tsShp = 	"{}.instObjGroups[0]".format(geoShp)
	cmds.connectAttr(tsShp, "{0}.input[{1}].inShape".format(ts, i))
	cmds.connectAttr("{}.outColor".format(fileNode), "{0}.input[{1}].inTriple".format(ts, i)) 
	
# delete pNode and tNode
cmds.delete(pNode, tNode)

# worry about length switch later when we populate the file node itself 