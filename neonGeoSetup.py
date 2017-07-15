import maya.cmds as cmds
import maya.mel as mel
import zTools.zbw_rig as rig
reload(rig)
import os
from functools import partial

# UI - option to create mesh light (CBG)

# some tag in houdini that if the shape has it, just put it in the ctrl and don't do all the fancy stuff to it

# duplicate live geo stuff (and neonize them?)

widgets = {}

def neon_geo_UI(*args):
	if cmds.window("neonWin", exists=True):
		cmds.deleteUI("neonWin")

	widgets["win"] = cmds.window("neonWin", t="neon geo setup", w=350, h=200, rtf=True)
	widgets["clo"] = cmds.columnLayout(w=350, h=200)
	widgets["camTFBG"] = cmds.textFieldButtonGrp(l="RenderCam", cw=[(1, 70),(1, 150),(1, 70)], cal=[(1,"left"),(1, "left"),(1, "left")], bl="<<<", bc=populate_camera)
	widgets["mainTLO"] = cmds.tabLayout()

	widgets["importCLO"] = cmds.columnLayout("Alembic Stuff", w=350)
	cmds.button(l="import alembic", w=350, h=30, bgc=(.5, .7, .5), c=import_abc)
	cmds.separator(h=10)
	cmds.text("Select alembics you want to split out")
	cmds.button(l="seperate abc into xforms based on their shapes", w=350, h=30, bgc=(.7, .7, .5), c=separate_abc)
	cmds.separator(h=10)
	cmds.text("select alembic (or static) geo to 'neon-ize'")
	widgets["lightCBG"] = cmds.checkBoxGrp(l="create a redshift meshlight?", ncb=1, cw=[(1, 150), (2, 50)], cal=[(1, "left"), (1, "left")], v1=False)
	cmds.separator(h=5)	
	cmds.button(l="duplicate abc's into neon setup", w=350, h=30, bgc=(.7, .5, .5), c=dupe_abc)	

	cmds.setParent(widgets["mainTLO"])
	widgets["regGeoCLO"] = cmds.columnLayout("Live Geo", w=350)
	cmds.text("Do this stuff with live geo in the scene (like lines, etc)")
	cmds.button(l="dupe geo and neonize it", w=350, h=30, bgc=(.7, .7, .5), c=dupe_live_geo)

	cmds.setParent(widgets["mainTLO"])
	widgets["shaderCLO"] = cmds.columnLayout("Shaders", w=350)
	cmds.text("assign shaders to slots, you can then\nassign them indiv to objs or\nto an abc control to do it all", al="left")
	widgets["firstGlassTFBG"] = cmds.textFieldButtonGrp(l="glassShd", cw=[(1, 70),(1, 150),(1, 70)], cal=[(1,"left"),(1, "left"),(1, "left")], bl="<<<", bc=partial(populate_shader, "firstGlassTFBG"))
	widgets["firstNeonTFBG"] = cmds.textFieldButtonGrp(l="neonShd", cw=[(1, 70),(1, 150),(1, 70)], cal=[(1,"left"),(1, "left"),(1, "left")], bl="<<<", bc=partial(populate_shader, "firstNeonTFBG"))
	cmds.separator(h=5)
	cmds.rowColumnLayout(nc=2, cw=[(1, 160), (2, 160)], cs=[(1,0),(2,20)])
	cmds.button(l="indiv asgn glass", w=160, h=20, bgc=(.9, .4, .4), c=partial(shaders_geo, "firstGlassTFBG"))
	cmds.button(l="indiv asgn neon", w=160, h=20, bgc=(.8, .3, .3), c=partial(shaders_geo, "firstNeonTFBG"))
	cmds.setParent(widgets["shaderCLO"])
	cmds.separator(h=5)	
	cmds.button(l="assign to sel abc ctrl", w=350, h=20, bgc=(.7, .5, .5), c=partial(shaders_abc, 1))
	cmds.separator(h=10)
	widgets["secondGlassTFBG"] = cmds.textFieldButtonGrp(l="glassShd2", cw=[(1, 70),(1, 150),(1, 70)], cal=[(1,"left"),(1, "left"),(1, "left")], bl="<<<", bc=partial(populate_shader, "secondGlassTFBG"))
	widgets["secondNeonTFBG"] = cmds.textFieldButtonGrp(l="neonShd2", cw=[(1, 70),(1, 150),(1, 70)], cal=[(1,"left"),(1, "left"),(1, "left")], bl="<<<", bc=partial(populate_shader, "secondNeonTFBG"))
	cmds.separator(h=5)
	cmds.rowColumnLayout(nc=2, cw=[(1, 160), (2, 160)], cs=[(1,0),(2,20)])
	cmds.button(l="indiv asgn glass", w=160, h=20, bgc=(.4, .9, .4), c=partial(shaders_geo, "secondGlassTFBG"))
	cmds.button(l="indiv asgn neon", w=160, h=20, bgc=(.5, .8, .3), c=partial(shaders_geo, "secondNeonTFBG"))
	cmds.setParent(widgets["shaderCLO"])	
	cmds.separator(h=5)
	cmds.button(l="assign to sel abc ctrl", w=350, h=20, bgc=(.5, .7, .5), c=partial(shaders_abc, 2))	
	cmds.separator(h=10)
	widgets["thirdGlassTFBG"] = cmds.textFieldButtonGrp(l="glassShd3", cw=[(1, 70),(1, 150),(1, 70)], cal=[(1,"left"),(1, "left"),(1, "left")], bl="<<<", bc=partial(populate_shader, "thirdGlassTFBG"))
	widgets["thirdNeonTFBG"] = cmds.textFieldButtonGrp(l="neonShd3", cw=[(1, 70),(1, 150),(1, 70)], cal=[(1,"left"),(1, "left"),(1, "left")], bl="<<<", bc=partial(populate_shader, "thirdNeonTFBG"))
	cmds.separator(h=5)
	cmds.rowColumnLayout(nc=2, cw=[(1, 160), (2, 160)], cs=[(1,0),(2,20)])
	cmds.button(l="indiv asgn glass", w=160, h=20, bgc=(.4, .5, .8), c=partial(shaders_geo, "thirdGlassTFBG"))
	cmds.button(l="indiv asgn neon", w=160, h=20, bgc=(.4, .3, .8), c=partial(shaders_geo, "thirdNeonTFBG"))
	cmds.setParent(widgets["shaderCLO"])
	cmds.separator(h=5)	
	cmds.button(l="assign to sel abc ctrl", w=350, h=20, bgc=(.4, .5, .7), c=partial(shaders_abc, 3))	
	
	cmds.window(widgets["win"], e=True, rtf=True, w=5, h=5)
	cmds.showWindow(widgets["win"])


def dupe_abc(*args):
	"""
	creates a rig structure of the alembic objs with texture deformers added, etc and parents to camera
	"""
	cam = camera_check()
	if not cam:
		cmds.warning("no camera selected in window")

	sel = cmds.ls(sl=True)
	ctrlList = []

	rslight = cmds.checkBoxGrp(widgets["lightCBG"], q=True, v1=True)
	if rslight:
		rig.plugin_load("redshift4maya")

	tubes = [x for x in sel if not x.endswith("plane")]

	for geo in tubes:
		geoName = geo
		neon = cmds.duplicate(geo, rr=True, un=True, name="{0}_neonInner".format(geo))[0]
		lightmesh = cmds.duplicate(geo, rr=True, un=True, name="{0}_lightOuter".format(geo))[0]
		geo = cmds.rename(geo, "{0}_glass".format(geo))

		##### OUTER LIGHT
		cmds.select(lightmesh, r=True)
		lmTDef, lmTxform = cmds.textureDeformer(offset=0.0075, vectorSpace="Object", direction="Normal", pointSpace="UV", name="{0}_textureDef".format(lightmesh))
		lmTextTrans = cmds.rename(lmTxform, "{0}_lightmesh_TextureDef".format(geo))
		cmds.setAttr("{0}.texture".format(lmTDef), 1, 1, 1)
		outerShpOrig = cmds.listRelatives(lightmesh, s=True, f=True)[0]
		outerShp = cmds.rename(outerShpOrig, "{0}_shape".format(lightmesh))
		outerShpAttrs = ["rsAOCaster", "rsSelfShadows", "rsShadowReceiver", "rsShadowCaster", "rsSecondaryRayVisible", "rsPrimaryRayVisible", "rsGiVisible", "rsCausticVisible", "rsGiCaster"]
		for attr in outerShpAttrs:
			cmds.setAttr("{0}.rsEnableVisibilityOverrides".format(outerShp), 1)
			cmds.setAttr("{0}.{1}".format(outerShp, attr), 0)

		### GLASS
		cmds.select(geo)
		gTDef, gTxform = cmds.textureDeformer(offset=0.00, strength=0.00, vectorSpace="Object", direction="Normal", pointSpace="Local", name="{0}_textureDef".format(geo))
		gTextTrans = cmds.rename(gTxform, "{0}_glass_TextureDef".format(geo))
		cmds.setAttr("{0}.texture".format(gTDef), 1, 1, 1)

		#### NEON
		cmds.select(neon, r=True)
		nTDef, nTxform = cmds.textureDeformer(offset=-0.05, strength=0.02, vectorSpace="Object", direction="Normal", pointSpace="Local", name="{0}_textureDef".format(neon))
		nTextTrans = cmds.rename(nTxform, "{0}_neon_TextureDef".format(geo))
		innerShpOrig = cmds.listRelatives(neon, s=True, f=True)[0]
		innerShp = cmds.rename(innerShpOrig, "{0}_shape".format(neon))
		innerShpAttrs = ["rsShadowReceiver", "rsShadowCaster"]
		for attr in innerShpAttrs:
			cmds.setAttr("{0}.rsEnableVisibilityOverrides".format(innerShp), 1)
			cmds.setAttr("{0}.{1}".format(innerShp, attr))

		noiseText = cmds.shadingNode("fractal", asTexture=True, name="{0}_fractal".format(neon))
		noisePlace = cmds.shadingNode("place2dTexture", asUtility=True, name= "{0}_factalPlace".format(neon))
		cmds.connectAttr("{0}.outUV".format(noisePlace), "{0}.uv".format(noiseText))
		cmds.connectAttr("{0}.outUvFilterSize".format(noisePlace), "{0}.uvFilterSize".format(noiseText))
		cmds.connectAttr("{0}.outColor".format(noiseText), "{0}.texture".format(nTDef), force=True)

		# light and finishing up
		if rslight:
			# make the red shift physical light and connect it to the outer geo. . . Set some init values on that
			lighttmp = mel.eval( "redshiftCreateLight(\"RedshiftPhysicalLight\")" )
			physLight = "{0}_meshlight".format(geoName)
			physLight = cmds.rename(lighttmp, physLight)
			physLightShp = cmds.listRelatives(physLight, s=True)[0]
			# move light to camera
			rig.snapTo(lightmesh, physLight)
			cmds.setAttr("{0}.v".format(physLight), 0)
			# cmds.setAttr("{0}.areaShape".format(physLightShp), 4)
			# link the light with lightmesh (HOW THE HELL TO DO THIS?)

		# add controls to the main geo
		ctrl = rig.createControl(type="star", color="red", axis="y", name="{0}_CTRL".format(geoName))
		ctrlShp = cmds.listRelatives(ctrl, s=True)[0]
		rig.snapTo(cam, ctrl)
		objList = [lmTextTrans, nTextTrans, gTextTrans, neon, lightmesh, geo]
		if rslight:
			objList.append(physLight)
		cmds.parent(objList, ctrl)
		cmds.parent(ctrl, cam)
		cmds.setAttr("{0}.v".format(lightmesh), 0)

		cmds.addAttr(ctrl, ln="thisCtrlVis", at="short", min=0, max=1, dv=0, k=True)
		cmds.addAttr(ctrl, ln="lightMeshTxStrength", at="float", min=0, max=1.0, dv=0.00, k=True)
		cmds.addAttr(ctrl, ln="neonTxStrength", at="float", min=0, max=1.0, dv=0.02, k=True)
		cmds.addAttr(ctrl, ln="glassTxStrength", at="float", min=0, max=1.0, dv=0.0, k=True)
		cmds.addAttr(ctrl, ln="lightMeshTxOffset", at="float", min=-1.0, max=1.0, dv=0.0075, k=True)
		cmds.addAttr(ctrl, ln="neonTxOffset", at="float", min=-1.0, max=1.0, dv=-0.03, k=True)
		cmds.addAttr(ctrl, ln="glassTxOffset", at="float", min=-1.0, max=1.0, dv=0.00, k=True)

		cmds.connectAttr("{0}.thisCtrlVis".format(ctrl), "{0}.visibility".format(ctrlShp))
		cmds.connectAttr("{0}.lightMeshTxStrength".format(ctrl), "{0}.strength".format(lmTDef))
		cmds.connectAttr("{0}.neonTxStrength".format(ctrl), "{0}.strength".format(nTDef))
		cmds.connectAttr("{0}.glassTxStrength".format(ctrl), "{0}.strength".format(gTDef))
		cmds.connectAttr("{0}.lightMeshTxOffset".format(ctrl), "{0}.offset".format(lmTDef))
		cmds.connectAttr("{0}.neonTxOffset".format(ctrl), "{0}.offset".format(nTDef))
		cmds.connectAttr("{0}.glassTxOffset".format(ctrl), "{0}.offset".format(gTDef))

		ctrlList.append(ctrl)

	cmds.select(ctrlList, r=True)


def dupe_live_geo(*args):
	"""
	duplicates geo and adds the texture deformers to it
	"""
	sel = cmds.ls(sl=True, type="transform")
	for obj in sel:
		# dupeSpecial, input cons
		par = cmds.listRelatives(obj, p=True)
		if par:
			par = par[0]
		dupe = cmds.duplicate(obj, rr=True, ic=True)
		neon = cmds.rename(dupe, "{0}_neonGeo".format(obj))
		# apply texture defs to each, parent defXforms to parent
		tDef, tXform = cmds.textureDeformer(strength=0.02, offset=-0.05, vectorSpace="Object", direction="Normal", pointSpace="UV", name="{0}_textureDef".format(neon))
		textTrans = cmds.rename(tXform, "{0}_neon_TextureDef".format(obj))

		noiseText = cmds.shadingNode("fractal", asTexture=True, name="{0}_fractal".format(obj))
		noisePlace = cmds.shadingNode("place2dTexture", asUtility=True, name= "{0}_factalPlace".format(obj))
		cmds.connectAttr("{0}.outUV".format(noisePlace), "{0}.uv".format(noiseText))
		cmds.connectAttr("{0}.outUvFilterSize".format(noisePlace), "{0}.uvFilterSize".format(noiseText))
		cmds.connectAttr("{0}.outColor".format(noiseText), "{0}.texture".format(tDef), force=True)

		lightmeshtmp = cmds.duplicate(obj, rr=True, ic=True)
		lightmesh = cmds.rename(lightmeshtmp, "{0}_lgtMeshGeo".format(obj))
		cmds.select(lightmesh, r=True)
		lmTDef, lmTxform = cmds.textureDeformer(offset=0.007, strength=0, vectorSpace="Object", direction="Normal", pointSpace="UV", name="{0}_textureDef".format(lightmesh))
		lmTextTrans = cmds.rename(lmTxform, "{0}_lightmesh_TextureDef".format(obj))
		cmds.setAttr("{0}.texture".format(lmTDef), 1, 1, 1)
		outerShpOrig = cmds.listRelatives(lightmesh, s=True, f=True)[0]
		outerShp = cmds.rename(outerShpOrig, "{0}_shape".format(lightmesh))
		outerShpAttrs = ["rsAOCaster", "rsSelfShadows", "rsShadowReceiver", "rsShadowCaster", "rsSecondaryRayVisible", "rsPrimaryRayVisible", "rsGiVisible", "rsCausticVisible", "rsGiCaster"]
		for attr in outerShpAttrs:
			cmds.setAttr("{0}.rsEnableVisibilityOverrides".format(outerShp), 1)
			cmds.setAttr("{0}.{1}".format(outerShp, attr), 0)

		# make the red shift physical light and connect it to the outer geo. . . Set some init values on that
		lighttmp = mel.eval( "redshiftCreateLight(\"RedshiftPhysicalLight\")" )
		physLight = "{0}_meshlight".format(obj)
		physLight = cmds.rename(lighttmp, physLight)
		physLightShp = cmds.listRelatives(physLight, s=True)[0]
		# move light to camera
		rig.snapTo(lightmesh, physLight)
		if par:
			cmds.parent(physLight, par)
			cmds.parent(textTrans, par)
			cmds.parent(lmTextTrans, par)

		cmds.setAttr("{0}.v".format(physLight), 1)
		cmds.setAttr("{0}.t".format(physLight), 0, 0, 0)
		cmds.setAttr("{0}.r".format(physLight), 0, 0, 0)
		cmds.setAttr("{0}.s".format(physLight), 1, 1, 1)

		# cmds.setAttr("{0}.areaShape".format(physLightShp), 4)
		# link the light with lightmesh (HOW THE HELL TO DO THIS?)


def get_sg(shd, *args):
	"""
	gets and returns shading group associated with a given shader
	"""
	sgs = cmds.listConnections(shd, type="shadingEngine")
	if sgs:
		return(sgs[0])
	else:
		return(False)


def assign_shader(geo, sg, *args):
	"""
	justs assigns the geo to the sg set
	"""
	cmds.sets(geo, e=True, forceElement=sg)


def shaders_geo(tfbg, *args):
	"""
	just assigns the shader from the tfbg to all selected geo
	"""
	shd = cmds.textFieldButtonGrp(widgets[tfbg], q=True, tx=True)
	sg = ""

	if shd:
		sg = get_sg(shd)

	if not sg:
		cmds.warning("shader name or shading group doesn't seem valid: {0}".format(shd))
		return()

	sel = cmds.ls(sl=True, type="transform")
	for obj in sel:
		shp = cmds.listRelatives(obj, s=True)
		for s in shp:
			typ = cmds.objectType(s)
			if typ == "mesh" or typ == "nurbsSurface":
				assign_shader(s, sg)


def shaders_abc(shdIndex, *args):
	"""
	parse out the objects in the ctrl hier and assign shaders to them
	"""
	sel = cmds.ls(sl=True)
	# get the relevant shaders (sgs)
	if shdIndex == 1:
		gKey = "firstGlassTFBG"
		nKey = "firstNeonTFBG"
	if shdIndex == 2:
		gKey = "secondGlassTFBG"
		nKey = "secondNeonTFBG"
	if shdIndex == 3:
		gKey = "thirdGlassTFBG"
		nKey = "thirdNeonTFBG"

	glassShd = cmds.textFieldButtonGrp(widgets[gKey], q=True, tx=True)
	neonShd = cmds.textFieldButtonGrp(widgets[nKey], q=True, tx=True)
	if glassShd:
		gsg = get_sg(glassShd)
	else:
		cmds.warning("you're missing an shader in a slot!")
		return()

	if neonShd:
		nsg = get_sg(neonShd)
	else:
		cmds.warning("you're missing an shader in a slot!")
		return()
	if not gsg and nsg:
		cmds.warning("doesn't seem like you have two valid shaders (or at least not shading groups for those)")
		return()

	for ctrl in sel:
		chldn = cmds.listRelatives(ctrl, c=True, type="transform")
		for chld in chldn:
			if chld.rpartition("_")[2] == "glass":
				shp = cmds.listRelatives(chld, s=True)
				for s in shp:
					assign_shader(s, gsg)
			if chld.rpartition("_")[2] == "neonInner":
				shp = cmds.listRelatives(chld, s=True)
				for s in shp:
					assign_shader(s, nsg)


def populate_shader(tfbg, *args):
	sel = cmds.ls(sl=True)
	if len(sel) != 1:
		cmds.warning("need to select 1 shader!")
		return()
	cmds.textFieldButtonGrp(widgets[tfbg], e=True, tx=sel[0])


def separate_abc(*args):
	"""
	seperates abcs into xforms and parents them under the camera and moves them to (appox) image plane location
	"""
	cam = camera_check()
	if not cam:
		cmds.warning("need to select your render cam in the window (top of window)")
	sel = cmds.ls(sl=True)

	if not sel:
		cmds.warning("no abc selected!")
		return()
	outGeoList = []
	
	for abc in sel:
		hold = False
		if rig.isType(abc, "mesh"):
			shps = [x for x in cmds.listRelatives(abc, s=True)]
			pos = cmds.xform(abc, ws=True, q=True, rp=True)
			par = ""
			parList = cmds.listRelatives(abc, p=True)
			if parList:
				if parList[0] != cam:
					parent_and_zero(sel)
				par = parList[0]
			for shp in shps:
				nShp=cmds.rename(shp, "{0}Shape".format(shp))
				xf = cmds.group(em=True, name=shp)
				cmds.xform(xf, ws=True, t=pos)
				cmds.parent(nShp, xf, r=True, s=True)
				if par:
					cmds.parent(xf, par)
				cmds.setAttr("{0}.t".format(xf), 0,0,0) 
				cmds.setAttr("{0}.r".format(xf), 0,0,0) 
				cmds.setAttr("{0}.s".format(xf), 1,1,1) 

				cmds.setAttr("{0}.t".format(xf), 0, -5.371, -18.684)

				outGeoList.append(xf)
		else:
			cmds.warning("{0} is not a mesh. Skipping!".format(abc))	
			hold = True

		if not hold:
			cmds.delete(abc)
	
	cmds.select(outGeoList)


def parent_and_zero(sel, *args):
	"""
	parents the geo to the cam and zeroes it out
	"""
	cam = camera_check()
	cmds.parent(sel, cam)
	for obj in sel:
		cmds.setAttr("{0}.t".format(obj), 0,0,0)
		cmds.setAttr("{0}.r".format(obj), 0,0,0)
		cmds.setAttr("{0}.s".format(obj), 1,1,1)


def import_abc(*args):
	"""
	imports abcs
	"""
	cam = camera_check()
	if not cam:
		cmds.warning("you need to select a camera to work from (top of window)")
		return()

	path = cmds.fileDialog2(fileMode=1, dialogStyle=1)
	if path:
		path = path[0]

	if os.path.splitext(path)[1] != ".abc":
		cmds.warning("that doesn't seem to be an '.abc' file")
		return()

	myabc = cmds.AbcImport(path, mode="import", reparent=cam)


def populate_camera(*args):
	"""
	puts the camera in the text field group for later stuff
	"""
	sel = cmds.ls(sl=True)
	if len(sel) != 1:
		cmds.warning("need to select 1 object!")
		return()

	if rig.isType(sel[0], "camera"):
		cmds.textFieldButtonGrp(widgets["camTFBG"], e=True, tx=sel[0])
	else:
		cmds.warning("that's not a camera!")


def camera_check(*args):
	"""
	make sure that a camera is in the textfield grp
	"""	
	cam = cmds.textFieldButtonGrp(widgets["camTFBG"], q=True, tx=True)
	if rig.isType(cam, "camera"):
		return(cam)
	else:
		return(False)


def neonGeoSetup(*args):
	neon_geo_UI()