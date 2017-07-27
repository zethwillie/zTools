import maya.mel as mel
import maya.cmds as cmds
import os
import zTools.zbw_rig as rig

"""
select the control obj, then all the geo tubes and run
"""

sel = cmds.ls(sl=True)
ctrl = sel[0]
objs = sel[1:]
for obj in objs:
	par = cmds.listRelatives(obj, p=True)[0]
	
	cmds.select(obj, r=True)
	gTDef, gTxform = cmds.textureDeformer(offset=-0.00, strength=0.00, vectorSpace="Object", direction="Normal", pointSpace="UV", name="{0}_glass_textDef".format(obj))
	gTextTrans = cmds.rename(gTxform, "{0}_glass_TextureDef".format(obj))
	cmds.setAttr("{0}.texture".format(gTDef), 1, 1, 1)

	neon = cmds.duplicate(obj, rr=True, ic=True, name="{0}_neon".format(obj))[0]
	cmds.select(neon, r=True)
	nTDef, nTxform = cmds.textureDeformer(offset=-0.00, strength=0.00, vectorSpace="Object", direction="Normal", pointSpace="UV", name="{0}_neon_textDef".format(obj))
	nTextTrans = cmds.rename(nTxform, "{0}_TextureDef".format(neon))
	
	noiseText = cmds.shadingNode("fractal", asTexture=True, name="{0}_fractal".format(neon))
	noisePlace = cmds.shadingNode("place2dTexture", asUtility=True, name= "{0}_fractalPlace".format(neon))
	cmds.connectAttr("{0}.outUV".format(noisePlace), "{0}.uv".format(noiseText))
	cmds.connectAttr("{0}.outUvFilterSize".format(noisePlace), "{0}.uvFilterSize".format(noiseText))
	cmds.connectAttr("{0}.outColor".format(noiseText), "{0}.texture".format(nTDef), force=True)
	
	##### OUTER LIGHT
	lightmesh = cmds.duplicate(obj, rr=True, ic=True, name="{0}_lgtMeshGeo".format(obj))[0]
	cmds.select(lightmesh, r=True)
	lmTDef, lmTxform = cmds.textureDeformer(strength=0, offset=0.0075, vectorSpace="Object", direction="Normal", pointSpace="UV", name="{0}_textureDef".format(lightmesh))
	lmTextTrans = cmds.rename(lmTxform, "{0}_lm_TextDef".format(obj))
	cmds.setAttr("{0}.texture".format(lmTDef), 1, 1, 1)
	outerShpOrig = cmds.listRelatives(lightmesh, s=True, f=True)[0]
	outerShp = cmds.rename(outerShpOrig, "{0}_shape".format(lightmesh))
	outerShpAttrs = ["rsAOCaster", "rsSelfShadows", "rsShadowReceiver", "rsShadowCaster", "rsSecondaryRayVisible", "rsPrimaryRayVisible", "rsGiVisible", "rsCausticVisible", "rsGiCaster"]
	for attr in outerShpAttrs:
		cmds.setAttr("{0}.rsEnableVisibilityOverrides".format(outerShp), 1)
		cmds.setAttr("{0}.{1}".format(outerShp, attr), 0)	

	lighttmp = mel.eval( "redshiftCreateLight(\"RedshiftPhysicalLight\")" )
	physLight = "{0}_meshlight".format(obj)
	physLight = cmds.rename(lighttmp, physLight)
	physLightShp = cmds.listRelatives(physLight, s=True)[0]
	# move light to camera
	rig.snapTo(lightmesh, physLight)
	cmds.setAttr("{0}.areaVisibleInRender".format(physLightShp), 0)
	cmds.setAttr("{0}.v".format(lightmesh), 0)
	cmds.setAttr("{0}.v".format(physLight), 0)

	# if attr doesn't exist
	if not cmds.attributeQuery("glassLineStrength", node = ctrl, exists=True):
		cmds.addAttr(ctrl, at="float", ln="glassLineStrength", min=0, max=5, k=True, dv=0)
	if not cmds.attributeQuery("glassLineOffset", node = ctrl, exists=True):
		cmds.addAttr(ctrl, at="float", ln="glassLineOffset", min=-1, max=1, k=True, dv=0)	
	if not cmds.attributeQuery("neonLineStrength", node = ctrl, exists=True):
		cmds.addAttr(ctrl, at="float", ln="neonLineStrength", min=0, max=5, k=True, dv=.02)
	if not cmds.attributeQuery("neonLineOffset", node = ctrl, exists=True):
		cmds.addAttr(ctrl, at="float", ln="neonLineOffset", min=-1, max=1, k=True, dv=-.03)
	if not cmds.attributeQuery("lightMeshLineStrength", node = ctrl, exists=True):
		cmds.addAttr(ctrl, at="float", ln="lightMeshLineStrength", min=0, max=5, k=True, dv=0.0)
	if not cmds.attributeQuery("lightMeshLineOffset", node = ctrl, exists=True):
		cmds.addAttr(ctrl, at="float", ln="lightMeshLineOffset", min=-1, max=1, k=True, dv=0.01)

	zeroAttr = ["glassLineStrength", "glassLineOffset", "lightMeshLineStrength"]
	for attr in zeroAttr:
		cmds.setAttr("{0}.{1}".format(ctrl, attr), 0)
	cmds.setAttr("{0}.neonLineStrength".format(ctrl), .02)
	cmds.setAttr("{0}.neonLineOffset".format(ctrl, -.03))
	cmds.setAttr("{0}.lightMeshLineOffset".format(ctrl, 0.01))	

	dm = cmds.shadingNode("decomposeMatrix", asUtility=True, name = "{0}_DM".format(obj))
	cmds.connectAttr("{0}.worldMatrix[0]".format(ctrl), "{0}.inputMatrix".format(dm))
	dmMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{0}_dmMult".format(obj))
	cmds.connectAttr("{0}.outputScale".format(dm), "{0}.input2".format(dmMult))
	cmds.connectAttr("{0}.neonLineStrength".format(ctrl), "{0}.input1X".format(dmMult))
	cmds.connectAttr("{0}.neonLineOffset".format(ctrl), "{0}.input1Y".format(dmMult))	
	cmds.connectAttr("{0}.outputX".format(dmMult), "{0}.strength".format(nTDef))
	cmds.connectAttr("{0}.outputY".format(dmMult), "{0}.offset".format(nTDef))
		
	cmds.connectAttr("{0}.glassLineStrength".format(ctrl), "{0}.strength".format(gTDef))
	cmds.connectAttr("{0}.glassLineOffset".format(ctrl), "{0}.offset".format(gTDef))
	cmds.connectAttr("{0}.lightMeshLineStrength".format(ctrl), "{0}.strength".format(lmTDef))
	cmds.connectAttr("{0}.lightMeshLineOffset".format(ctrl), "{0}.offset".format(lmTDef))


	if par:
		cmds.parent(nTextTrans, gTextTrans, lmTextTrans, physLight, par)

	objPos = cmds.getAttr("{0}.t".format(obj))[0]
	cmds.setAttr("{0}.t".format(physLight), objPos[0], objPos[1], objPos[2])
