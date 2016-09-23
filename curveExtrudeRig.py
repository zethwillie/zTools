import maya.cmds as cmds
import zbw_rig as rig

#---------------- length drives which file texture we use

widgets = {}

def curveExtrudeUI():
	if cmds.window("crvExtrRigWin", exists = True):
		cmds.deleteUI("crvExtrRigWin")

	width = 300
	widgets["win"] = cmds.window("crvExtrRigWin", t="curveExtrudeRig", w=width, sizeable=True, resizeToFitChildren=True)
	widgets["CLO"] = cmds.columnLayout()

#---------------- cap rig should be optional
	##### extrude ########
	widgets["extrudeFLO"] = cmds.frameLayout("1. Extrude Curve", w=300, cll=True, cl=False, bgc=(.2, .2,.2))
	widgets["extrCLO"] = cmds.columnLayout()	
	cmds.text(l = "select the profile curve, cap rig, and curves to\nhook up in that order!\nWARNING: This won't undo cleanly!", al="left")
	#cmds.text(l="========= rebuild crvs ===========")
	widgets["recoIFBG"] = cmds.intFieldGrp(l="Points/Unit:", nf = 1, cal = [(1, "left"), (2, "left")], v1= .1, en = False, cw=[(1, 70), (2, 50)])
	widgets["ctrlFFG"] = cmds.floatFieldGrp(l="Control Size (units)", nf=1, cal = [(1, "left"), (2, "left")], v1=20, cw=[(1, 100), (2, 50)])
	#widgets["keepCBG"] = cmds.checkBoxGrp(l="keep originals?", v1 = True, cal=[(1, "left"), (2, "left")], cw=[(1, 70), (2, 40)])
	#cmds.separator(h=10)
	#cmds.text(l="========= build rigs ===========")	
	widgets["rebuildBut"] = cmds.button(l="Build Rigs!", w = 300, h=35, bgc = (.5, .4, .4), c = extrude)
	cmds.separator(h=10)

	###### create textures #########
	cmds.setParent(widgets["CLO"])
	widgets["textureFLO"] = cmds.frameLayout("2. Create Textures and Switch", w=300, h=120, cll=True, cl=False, bgc=(.2, .2,.2))
	widgets["textCLO"] = cmds.columnLayout()
	cmds.text(l="Shift select the shader node and then all top level ctrls.\nThis will assign the shader and create a txt node for each\nand create a 3switch, then connect ctl 'rptHolder' to place2d's", al="left")
	cmds.separator(h=10)
	widgets["textBut"] = cmds.button(l="Create shader connections!", w=300, h=35, bgc=(.3,.5,.4), c=texture)	

	####### fill file textures ######
	cmds.setParent(widgets["CLO"])
	widgets["fileFLO"] = cmds.frameLayout("3. Replace File Textures", w=300, h=120, cll=True, cl=False, bgc=(.2, .2,.2))
	widgets["fileCLO"] = cmds.columnLayout()
#---------------- option to select from file instead of just from existing, change UI and function
	#widgets["fileRBG"] = cmds.radioButtonGrp(l="Where from?", nrb=2, sl=1, l1="existing txtr", l2="explore", cal=[(1, "left"),(2, "left"),(3, "left")], cw=[(1, 70), (2, 60),(3, 50)], cc=toggleFile)
	#cmds.separator(h=10)
	# widgets["fileFile"] = cmds.text(l="Select file from right side and then ctrl objs")
	# cmds.separator(h=10)
	widgets["selFile"] = cmds.text(l="Will populate the file nodes on textures.\nSelect a 'file' node with the correct file\n and then ctrl objs for curves", al="left")
	cmds.separator(h=10)
	widgets["fileBut"] = cmds.button(l="Populate connections!", w=300, h=35, bgc=(.5,.5,.4), c=fileLoad)	

	####### replace caps ######
	cmds.setParent(widgets["CLO"])
	widgets["capFLO"] = cmds.frameLayout("4. Replace cap rigs", w=300, h=120, cll=True, cl=False, bgc=(.2, .2,.2))
	widgets["capCLO"] = cmds.columnLayout()
	widgets["capText"] = cmds.text(l="Select the cap replacement obj, then ctrl objs\nfor curves. ", al="left")
	cmds.separator(h=10)
	widgets["capBut"] = cmds.button(l="Replace caps!", w=300, h=35, bgc=(.4,.5,.5), c=capReplace)	

	cmds.window(widgets["win"], e=True, h=100)
	cmds.showWindow(widgets["win"])

def toggleFile(*args):
	sel = cmds.radioButtonGrp(widgets["fileRBG"], q=True, sl=True)

	if sel == 1:
		cmds.text(widgets["selFile"], e=True, en=False)


def curveCheck(obj):
	""" takes object and returns true if it's a curve"""
	shpList = cmds.listRelatives(obj, shapes = True)
	if (not shpList) or (cmds.objectType(shpList[0]) != "nurbsCurve"):
		return False
	else:
		return True

def extrude(*args):

	sel = cmds.ls(sl=True, exactType = "transform")

	#keep = cmds.checkBoxGrp(widgets["keepCBG"], q=True, v1=True)

	if len(sel)<3:
		cmds.warning("You need to select the profile, then cap, then path curve in order!")
		return

	profileOrig = sel[0]
	cap = sel[1]
	curves = sel[2:]

	if not cmds.objExists("pastaRigSetupComponents_Grp"):
		cmds.group(empty=True, name="pastaRigSetupComponents_Grp")

	if not curveCheck(profileOrig):
		cmds.warning("Your first selection (profile) is not a curve!")
		return

	if not cmds.objExists("curveRebuild_originals_grp"):
		cmds.group(empty=True, name = "curveRebuild_originals_grp")

	cmds.parent("curveRebuild_originals_grp", "pastaRigSetupComponents_Grp")
	cmds.parent(profileOrig, cap, "pastaRigSetupComponents_Grp")	

	for curve in curves:
		if not curveCheck(curve):
			cmds.warning("{} is not a curve, skipping!".format(curve))

		else:
			profile = cmds.duplicate(profileOrig, name="{}_profileCrv".format(curve))[0]

			newCap = cmds.duplicate(cap, returnRootsOnly=True, rebuildType = 0, renameChildren=True, name="{}_capRig".format(curve))[0]
			# rigGrp = cmds.group(empty=True, name = "{}_rig_grp".format(curve))
			curveResults = rebuildCurve(curve)
			newCrv = curveResults[0]
			rebuild = curveResults[1]

			cmds.parent(curve, "curveRebuild_originals_grp")

			capAxis = "y"
			capUp = "z"

			ctrl = rig.createControl(type="sphere", name="{}_CTRL".format(curve), color="blue")
			ctrlScale(ctrl)
			capGrp = cmds.group(empty=True, name="{}_cap_grp".format(curve))
			deadGrp = cmds.group(empty=True, name="{}_noInherit_grp".format(curve))

			cmds.parent(deadGrp, ctrl)	
			#cmds.parent(ctrl, rigGrp)
			cmds.parent(newCap, capGrp)

			# add attrs to control
			cmds.addAttr(ctrl, ln="__xtraAttrs__", nn="__xtraAttrs__", at="bool", k=True)
			cmds.setAttr("{}.__xtraAttrs__".format(ctrl), l=True)
			cmds.addAttr(ctrl, ln="alongPath", at="float", min=0, max=100, k=True, dv=100.0)	
			cmds.setAttr("{}.alongPath".format(ctrl), 100)
			cmds.addAttr(ctrl, ln="geoVis", at="long", min=0, max=1, k=True, dv=1)
			cmds.addAttr(ctrl, ln="pathCurveVis", at="long", min=0, max=1, k=True, dv=1)
			cmds.addAttr(ctrl, ln="__curveStuff__", nn="__curveStuff__", at="bool", k=True)
			cmds.setAttr("{}.__curveStuff__".format(ctrl), l=True)
			cmds.addAttr(ctrl, ln="density", at="float", min=0.02, max=8, k=True, dv=0.05)
			cmds.addAttr(ctrl, ln="radiusDivisions", at="float", k=True, min=1, max=3, dv=1.0)		
			cmds.addAttr(ctrl, ln="reverseNormals", at="long", min=0, max=1, k=True)
			cmds.addAttr(ctrl, ln="capVisibility", at="long", min=0, max=1, k=True)
			cmds.setAttr("{}.capVisibility".format(ctrl), 1)
			cmds.addAttr(ctrl, ln="profileWidth", at="float", k=True, min=.001, max=3, dv=1.0)	
			cmds.addAttr(ctrl, ln="capWidth", at="float", k=True, min=.01, max=2.0, dv=1.0)	
			cmds.addAttr(ctrl, ln="capHeight", at="float", k=True, min=.01, max=2.0, dv=1.0)
			cmds.addAttr(ctrl, ln="rotateExtrusion", at="float", k=True, min=0, max=360)
			cmds.addAttr(ctrl, ln="rotateCap", at="float", k=True)
			cmds.addAttr(ctrl, ln="__textureAndRef__", nn="__textureAndRef__", at="bool", k=True)
			cmds.setAttr("{}.__textureAndRef__".format(ctrl), l=True)
			cmds.addAttr(ctrl, ln="textureRepeatMult", at="float", min = 0.01, dv= 1.0, k=True)		
			cmds.addAttr(ctrl, ln="length", at="float", k=True)
			initLen = cmds.arclen(newCrv, ch=False)
			cmds.setAttr("{}.length".format(ctrl), initLen)
			cmds.setAttr("{}.length".format(ctrl), l=True)

			cmds.addAttr(ctrl, ln="geo", at="message")
			cmds.addAttr(ctrl, ln="fileTexture", at="message")
			cmds.addAttr(ctrl, ln="capRig", at="message")
			cmds.connectAttr("{}.message".format(newCap), "{}.capRig".format(ctrl))

			# reference/driver attrs
			cmds.addAttr(ctrl, ln="prmHolder", at="float", k=True)
			cmds.addAttr(ctrl, ln="rptHolder", at="float", k=True)
			#cmds.setAttr("{}.radiusDivisions".format(ctrl), l=True)			

			# connect mult to path
			mult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{}_paraMult".format(curve))
			cmds.connectAttr("{}.alongPath".format(ctrl), "{}.input1X".format(mult))
			cmds.setAttr("{}.input2X".format(mult), 0.01)
			cmds.connectAttr("{}.profileWidth".format(ctrl), "{}.scaleX".format(profile))
			cmds.connectAttr("{}.profileWidth".format(ctrl), "{}.scaleZ".format(profile))

			# reverse for normals
			reverse = cmds.shadingNode("reverse", asUtility=True, name="{}_reverse".format(curve))
			cmds.connectAttr("{}.reverseNormals".format(ctrl), "{}.inputX".format(reverse))
			
			# cap, path and texture attrs and nodes
			cmds.connectAttr("{}.capVisibility".format(ctrl), "{}.v".format(capGrp))
			repeatMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{}_RptMult".format(curve))
			cmds.connectAttr("{}.outputX".format(mult), "{}.input1X".format(repeatMult))
			cmds.connectAttr("{}.textureRepeatMult".format(ctrl), "{}.input2X".format(repeatMult))
			cmds.connectAttr("{}.pathCurveVis".format(ctrl), "{}.visibility".format(newCrv))

			#connect the rebuild density
			densityMult = cmds.shadingNode("multiplyDivide", asUtility=True, name="{}_DensityMult".format(curve))
			cmds.connectAttr("{}.density".format(ctrl), "{}.input1X".format(densityMult))
			cmds.connectAttr("{}.length".format(ctrl), "{}.input2X".format(densityMult))
			cmds.connectAttr("{}.outputX".format(densityMult), "{}.spans".format(rebuild))

			cmds.connectAttr("{}.outputX".format(repeatMult), "{}.rptHolder".format(ctrl))
			cmds.connectAttr("{}.outputX".format(mult), "{}.prmHolder".format(ctrl))
			cmds.setAttr("{}.prmHolder".format(ctrl), l=True)
			cmds.setAttr("{}.rptHolder".format(ctrl), l=True)
			cmds.connectAttr("{}.capWidth".format(ctrl), "{}.scaleX".format(capGrp))
			cmds.connectAttr("{}.capWidth".format(ctrl), "{}.scaleZ".format(capGrp))
			cmds.connectAttr("{}.capHeight".format(ctrl), "{}.scaleY".format(capGrp))
			cmds.connectAttr("{}.rotateCap".format(ctrl), "{}.rotateY".format(newCap))

			# position control at start of curve
			startPos = cmds.pointOnCurve(curve, parameter = 0, position = True)
			cmds.xform(ctrl, ws=True, t=startPos)

			moPath = cmds.pathAnimation(capGrp, newCrv, fractionMode=True, follow=True, followAxis=capAxis, upAxis=capUp, worldUpType="scene", startTimeU=0.0, endTimeU=100.0)
			moPathAnimAttr = cmds.listConnections("{}.uValue".format(moPath), d=False, p=True)[0]

			start, end = getSliderRange()
			current = cmds.currentTime(q=True)
			cmds.currentTime(0)

			pPos = cmds.xform(capGrp, q=True, ws=True, rp=True)
			pRot = cmds.xform(capGrp, q=True, ws=True, ro=True)
			cmds.xform(profile, ws=True, t=pPos)
			cmds.xform(profile, ws=True, ro=pRot)

			cmds.currentTime(current)

			# extrude the curve
			extr = cmds.extrude(profile, newCrv, ch=True, range=True, polygon=True, extrudeType=2, useComponentPivot=True,
			                    fixedPath=True, useProfileNormal=True, reverseSurfaceIfPathReversed=True)
			extrGeo, extrNode = extr[0], extr[1]

			normal = cmds.polyNormal(extrGeo, normalMode=4, userNormalMode=0, ch=1)[0]
			cmds.connectAttr("{}.outputX".format(reverse), "{}.normalMode".format(normal))
			cmds.connectAttr("{}.message".format(extrGeo), "{}.geo".format(ctrl))
			cmds.connectAttr("{}.geoVis".format(ctrl), "{}.visibility".format(extrGeo))
			cmds.connectAttr("{}.rotateExtrusion".format(ctrl), "{}.rotation".format(extrNode))

			# get extrude connections
			connects = cmds.listConnections(extrNode)
			profNode, pathNode, tessNode = connects[0], connects[1], connects[2]

			# connect up stuff to extrusion
			cmds.connectAttr("{}.outputX".format(mult), "{}.maxValue".format(pathNode))
			cmds.connectAttr("{}.radiusDivisions".format(ctrl), "{}.uNumber".format(tessNode))
			cmds.parent(newCrv, ctrl)
			cmds.setAttr("{}.inheritsTransform".format(deadGrp), 0)
			cmds.parent(extrGeo, deadGrp)
			cmds.parent(profile, deadGrp)	
			cmds.setAttr("{}.v".format(profile), 0)
			cmds.parent(capGrp, deadGrp)

			# motion path stuff
			cmds.delete(moPathAnimAttr.partition(".")[0])
			cmds.connectAttr("{}.outputX".format(mult), "{}.uValue".format(moPath))
			cmds.setAttr("{}.visibility".format(cap))
			cmds.setAttr("{}.visibility".format(profileOrig))


def getSliderRange(*args):
	"""gets framerange in current scene and returns start and end frames"""

	# get timeslider range start
	startF = cmds.playbackOptions(query=True, min=True)
	endF = cmds.playbackOptions(query=True, max=True)

	return(startF, endF)

def ctrlScale(ctrl):
	scl = cmds.floatFieldGrp(widgets["ctrlFFG"], q=True, v1=True)/2
	cvs = cmds.ls("{}.cv[*]".format(ctrl), fl=True)
	cmds.select(cvs)
	cmds.scale(scl, scl, scl)
	cmds.select(clear=True)


def calculatePts(crv, *args):
	"""
	uses the window to get the number of pts that should be in the curve
	"""	
	cLen = cmds.arclen(crv, ch=False)
	perUnit = cmds.intFieldGrp(widgets["recoIFBG"], q=True, v1=True)
	total = cLen * perUnit

	return total

def rebuildCurve(curve, *args):
	""" 
		rebuilds selected curves to specs in window
	"""
	num = calculatePts(curve)
	newCrv = cmds.rebuildCurve(curve, rebuildType = 0, ch=1, spans = num, keepRange = 0, replaceOriginal = 0, name = "{}_RB".format(curve))
	cmds.setAttr("{}.v".format(curve), 0)

	return newCrv

def texture(*args):
	
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
		tsShp = "{}.instObjGroups[0]".format(geoShp)
		cmds.connectAttr(tsShp, "{0}.input[{1}].inShape".format(ts, i))
		cmds.connectAttr("{}.outColor".format(fileNode), "{0}.input[{1}].inTriple".format(ts, i)) 
		
		cmds.connectAttr("{}.message".format(fileNode), "{}.fileTexture".format(ctrls[i]))

	# delete pNode and tNode
	cmds.delete(pNode, tNode)

	# worry about length switch later when we populate the file node itself 

def fileLoad(*args):
	
	sel = cmds.ls(sl=True)
	origTexture = sel[0]
	ctrls = sel[1:]

	# get path
	path = cmds.getAttr("{}.fileTextureName".format(origTexture))
	if not path:
		cmds.warning("No file present in {}. Cancelling!".format(origTexture))
		return

	for ctrl in ctrls:
		ctrlFile = cmds.connectionInfo("{}.fileTexture".format(ctrl), sfd=True).partition(".")[0]

		# add path to ctrl file
		cmds.setAttr("{}.fileTextureName".format(ctrlFile), path, type="string")


def capReplace(*args):
	
	sel = cmds.ls(sl=True, type="transform")

	if sel < 2:
		cmds.warning("You don't have two things selected (cap and one ctrl minimum)!")
		return

	newCap = sel[0]
	ctrls = sel[1:]

	for ctrl in ctrls:
		oldCap = cmds.connectionInfo("{}.capRig".format(ctrl), sfd=True).partition(".")[0]
		
		dupe = rig.swapDupe(newCap, oldCap, delete=True, name=oldCap)

		cmds.connectAttr("{}.rotateCap".format(ctrl), "{}.rotateY".format(dupe))

	# if not already, parent cap replace obj in folder and hide
	par = cmds.listRelatives(newCap, p=True)
	if not par or par[0] != "pastaRigSetupComponents_Grp":
		cmds.parent(newCap, "pastaRigSetupComponents_Grp")

	cmds.setAttr("{}.v".format(newCap), 0)


def curveExtrude():
	curveExtrudeUI()
