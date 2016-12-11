import maya.cmds as cmds
import maya.mel as mel
import os, sys,	subprocess
from shutil import copyfile
from functools import partial
import chrlx_pipe.chrlxFuncs as cFuncs
reload(cFuncs)
import chrlx_pipe.chrlxClash as cClash
reload(cClash)

##############
# functions and such for the mastering process of assets
# some separate processes for geo and rigs
# uses chrlxFuncs to do general things 
##############

#check that we're in the right scene
# do master stuff
# rename this to master
# save master and open new, open ws or open master

######### open separate window to promote past version to current master, (save ws version somewhere in scene? Scene info)
######### this woudl be ws version itself for ws's and ws version for masters

mWidget = {}


######### all of masterAsset AFTER button click? this will allow us to push through
def masterAsset(asset, assFolder, fType, *args):
	"""gets latest version of past_versions, args: assetName, assFolder (i.e. rig folder, lgt var folder, etc) fType (i.e. 'lgt', 'anm', 'geo', etc)"""

	masterFile = "{0}_{1}".format(asset, fType)

	latestMasterVersion = cFuncs.getLastAssetMasterVersion(asset, assFolder, fType, *args) #check if there's a master
	latestWorkshop = cFuncs.getLatestAssetWS(asset, assFolder, fType) #check the lastest workshop

	if latestMasterVersion and (latestMasterVersion != "Abort"):
		num = int(os.path.basename(latestMasterVersion).rstrip(".ma").rpartition("_v")[2])
		incrNum = "{:0>3d}".format(num + 1)

	elif latestMasterVersion == "Abort":
		cmds.warning("masterFuncs.masterAsset: There was some kind of issue with the paths to get the latest master for backup")
		return
	
	elif latestMasterVersion == None:
		incrNum = "001"
	
	#create file name and full path
	newPastVersion = "{0}/{1}/past_versions/{2}_v{3}.ma".format(assFolder, fType, masterFile, incrNum)

	# does this line up with the ws file structure? 	
	check = cFuncs.checkCurrentMasterMatch(asset, fType)

	if not check:
		#here we bail out if current scene isn't workshop of the scene you're trying to master (from window)
		cmds.confirmDialog(t="SCENE MISMATCH", m="Your current scene doesn't line up\nwith the asset you've selected\nin the asset window. . . \n\nMake sure you're in a workshop file\nfor the asset you want to master!")
		return "FILE MISMATCH - NO MASTER CREATED!"

	#copy current master to past masters and rename to new num 
	currentMaster = "{0}/{1}/{2}.ma".format(assFolder, fType, masterFile)
	destination = "{}".format(newPastVersion)
	currentWS = cmds.file(q=True, sceneName = True)
	
########### save current scene as latest workshop - note: "MASTERING - ".format(currentWS)  is there a way to do this??? pass a note? maybe use an arg (bool) in to tell whether to use UI stuff
############ basically this should call master win !!!!!! and all below is "IF" that win lets us proceed. . . 

######### --- need to sort out fType for fileinfo mastering of rig file, right now it says "geo" in file info
	#increment ws file from current
	newWSFile = "{}.ma".format(cFuncs.incrementWS(asset, assFolder, fType))
	cFuncs.putFileInfo(fType, incrNum, note = "Mastering!")
	cmds.file(rename = newWSFile)
	cmds.file(save=True, type="mayaAscii")

	#do the mastering stuff to the current file, if we bail at any stage, reopen the ws and don't save master
	cmds.file(rename=currentMaster)
	if fType == "geo":
		masterTest = masterGeo(asset, assFolder)
		if masterTest == "AbortC":
			print "trying to get latest ws file: {}".format(newWSFile)
			cmds.file(newWSFile, open=True, force=True )
			return("Failed mastering at geo cleanup phase. Try again after fixing problems")

	if fType == "rig":
		masterTest = masterRig(asset, assFolder)
		if masterTest == "AbortC":
			cmds.file(latestWorkshop, open=True, force=True )
			return("Failed mastering at rig cleanup phase. Try again after fixing problems")

	if os.path.isfile(currentMaster): #check if there is a master file currently. If so, move it to the past versions
		os.rename(currentMaster, destination)
		print "masterAsset.masterAsset:\n------ moving: {0} \n------ to: {1}".format(currentMaster, destination)

	cmds.file(save=True, type="mayaAscii")

	if fType == "geo":
		#check if there's a rig workshop for this asset
		rigWS = cFuncs.getLatestAssetWS(asset, assFolder, "rig")
		print "workshop rig file is:", rigWS
		if not (rigWS and os.path.exists(rigWS)):
			#HERE THROW UP A DIALOG ASKING WHETHER WE WANT TO CONTINUE ON THROUGH RIG
			print "-------Starting creation of rig files-------"
			initializeRigWS(asset, assFolder, "rig")

		else:
			print "A RIG WS EXISTS: {}".format(rigWS)

	#refresh the asset info in the asset win
	if cmds.window("assetWin", exists=True):
		import chrlx_pipe.assetWin as assWin
		assWin.populateWindow()

	return "Master created successfully: {0}".format(currentMaster)

def masterGeo(asset, assetFolder, *args):
	#make sure to stick info about the relevant workshop into the file for the "promotePastVersion" function later (promote them both)

	# make saving a note mandatory, BUT make sure this DOESN"T require user input when in headless mode (maybe just an arg to pass)
	#bring up window
	print "\n-------------------\nDOING MASTER GEO STUFF HERE!\n-------------------"
	clean = cleanAssetScene("geo")
	if clean == "Abort":
		return("AbortC")

####### ------ tag this master with the workshop num to compare to latest?
###### ------ if not mastering through, option to either go to new scene or open master?

def initializeRigWS(asset, assetFolder, *args):
	"""will use standalone maya to create the initial rig ws file"""	
################ ------------ use env variables to get these paths
	print "INITIALIZING RIG WORKSHOP"
	try:	
		subprocess.call(["C:/Program Files/Autodesk/Maya2016/bin/mayapy.exe","H:/development/3D/maya/maya2015/scripts/chrlx_pipe/buildInitialRigFiles.py", asset, assetFolder])
		print "FINISHED WITH RIG WS CREATION"
	except:
		print "DID NOT CREATE RIG WS"

def masterRig(asset, assetFolder, *args):
	#make sure to stick info about the relevant workshop into the file for the "promotePastVersion" function later (promote them both)
	# Should group geo and put it group under the controller to start!!! (this will allow for auto-mastering)
	# need to check whether there already is a scene in the ws folder? If not then go through geo ref process (prefix, setup, etc)

	#make a copy from reffed geo, group it 
	# import geo file from reference. . . 
	print "\n-------------------\nDOING MASTER RIG STUFF HERE!\n-------------------"
	######## - am I returning something below?
	clean = cleanAssetScene("rig") 
	if clean == "Abort":
		return("AbortC")

	# tag this master with the current rig ws to compare later. Also tag with latest geo ws? compare that too? 

def cleanAssetScene(fType, *args):	
	"""cleans up the stuff in the scene (deletes unwanted stuff, etc)"""
#generically to geo and rig files
	#remove namespaces
	ns = cFuncs.removeNamespace()
	print "removed namespaces: {}".format(ns)
	
	cfix = 1 #1 = fix the clashes, 0 = just report the clashes
	cClash.clash(cfix)

	# clean up the delete set
	if cmds.objExists("deleteSet"):
		delStuff = cmds.sets("deleteSet", q=True)
		cmds.delete(delStuff)
		try:
			cmds.delete("deleteSet")
		except:
			print "Problem deleting the deleteSet"

######### make sure all refs are loaded. . . 
	#import all refs
	refs =  cmds.file(q=True, r=True)
	for ref in refs:
		refNode = cmds.referenceQuery(ref, rfn=True)
		cmds.file(rfn=refNode, ir=True)

	#delete image planes
	ip = cmds.ls(type="imagePlane")
	print "deleting image planes: {}".format(ip)
	if ip:
		cmds.delete(ip)
	
	#delete camera bookmarks
	bm = cmds.ls(type = "cameraView")
	print "deleting camera bookmarks: {}".format(bm)
	if bm:
		cmds.delete(bm)

	#get all lights and delete
	lights = cFuncs.getLightList()
	print "deleting lights: {}".format(lights)
	if lights:
		cmds.delete(lights)

	#get extra cameras and delete
	cams = cFuncs.getCamList()
	print "deleting non-default cameras: {}".format(cams)
	if cams:
		cmds.delete(cams)
	
	#delete all TIME BASED anim curves (not setdriven keys)
	anmsT = cmds.ls(type = ("animCurveTL", "animCurveTU", "animCurveTA", "animCurveTT"))
	if anmsT:
		print "deleting time-based anim curves: {}".format(anmsT)
		cmds.delete(anmsT)

	#get rid of display layers, render layers, anm layers
	dl = cmds.ls(type="displayLayer")
	if dl:
		dl.remove("defaultLayer")
		print "deleting display layers: {}".format(dl)
		cmds.delete(dl)

	rl = cmds.ls(type = "renderLayer")
	if rl:
		rl.remove("defaultRenderLayer")
		print "deleting render layers: {}".format(rl)
		cmds.delete(rl)

	al = cmds.ls(type = "animLayer")
	if al:
		al.remove("BaseAnimation")
		print "deleting anim layers: {}".format(al)
		cmds.delete(al)

	#delete unknown nodes
	uk = cmds.ls(type = "unknown")
	if uk:
		print "deleting unknown nodes: {}".format(uk)
		cmds.delete(uk)

	#check for shaders? delete unused (following doesn't work wo a UI)
	#mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
	
	#grab list of all transforms
	allGeo = cmds.listRelatives(cmds.ls(geometry = True), p=True)
	#remove lattices from list
	for g in allGeo:
		if cmds.listRelatives(g, shapes=True, type="lattice"):
			allGeo.remove(g)

	allTransforms = cmds.ls(type = "transform")

	#get rid of face assigments (select only the first shader assigned)
	for geo in allGeo:
		shps = cmds.listRelatives(geo, s=True)
		if shps:
			for shp in shps:
				sg = cmds.listConnections(shp, type="shadingEngine")
				if (sg and len(sg) > 1):
					cmds.sets(geo, e=True, forceElement=sg[0]) 
					print "Found more than one shader on {0}. Reassigning to {1}".format(geo, sg[0])		
	
#if geo file . . . 
	if fType == "geo":

		#delete history on all geo objects
		cmds.delete(allGeo, ch=True)
		
		#delete deformers left over (should be none)
		# for geo in allGeo:
		# 	df = mel.eval("findRelatedDeformer {}".format(geo))
		# 	if df:
		# 		print "deleting deformers: {}".format(df)
		# 		cmds.delete(df)

		#parent all transforms to world
		for i in allGeo:
			print "------ {}".format(i)
			if cmds.listRelatives(i, p=True):
				cmds.parent(i, world=True)
	
		#delete constraints
		cnstrs = cmds.ls(type="constraint")
		print "deleting constraints: {}".format(cnstrs)
		if cnstrs:
			cmds.delete(cnstrs)
		
		#delete all sets
		removeSets = ["defaultLightSet", "defaultObjectSet"]
		setList = cmds.ls(et = "objectSet")
		for rmSt in removeSets:
			setList.remove(rmSt)
		if setList:
			cmds.delete(setList)

		#delete all expressions
		exprs = cmds.ls(type="expression")
		print "deleting expressions: {}".format(exprs)
		if exprs:
			cmds.delete(exprs)

		#delete all UNIT BASED anim curves (sdks, etc)
		sdkAnms = cmds.ls(type = ("animCurveUL", "animCurveUU", "animCurveUA", "animCurveUT"))
		if sdkAnms:
			print "deleting unit-based anim curves: {}".format(sdkAnms)
			cmds.delete(sdkAnms)
		
		allTransforms = cmds.ls(type = "transform")	

		#delete groups - because DAG should be flattened we can just delete a transform w/o children
		grps = [x for x in allTransforms if not cmds.listRelatives(x, shapes=True)]
		if grps:
			print "deleting empty groups: {}".format(grps)
			cmds.delete(grps)
		
		allTransforms = cmds.ls(type = "transform")
		#delete connections(should be no more anim, constraints at this point, so these would be direct connections) 
		for trans in allTransforms:
			#disconnect all channelbox channels
			cons = cmds.listConnections(trans, plugs=True, s=True)

			if cons:
				for con in cons:
					dest = cmds.connectionInfo(con, dfs=True)[0]
					cmds.disconnectAttr(con, dest)
		
		#freeze transforms on geo
		print "Freezing all geo objects"
		cmds.makeIdentity(allGeo, apply=True)
		
		#delete all namespaces
		cFuncs.removeNamespace()

		#check for "geo_" name - warn out of this
		geoName = cmds.ls("geo_*")
		if geoName:
			cmds.warning("the following objects have 'geo_' as their prefix!\n{}".format(geoName))

		#set displaySmoothness to 3
		cmds.displaySmoothness(allGeo, polygonObject = 1)

		#set ctrl size node
		if cmds.objExists("*ctrlSizeTemplateCrv"):
			ctrl = cmds.ls("*ctrlSizeTemplateCrv")[0]
			#measure distance (10.421 is scale 1)
			pos6 = cmds.pointPosition("{}.cv[6]".format(ctrl))
			pos18 = cmds.pointPosition("{}.cv[18]".format(ctrl))
			dist = pos6[0]-pos18[0]
			factor = dist/10.421


			rigScale = cmds.shadingNode("multiplyDivide", asUtility=True, n="RIGDATA")
			cmds.addAttr(rigScale, ln="scaleCtrl", at="float", dv=1.0)
			cmds.setAttr("{}.scaleCtrl".format(rigScale), factor)
			cmds.delete(ctrl)

#if rig file . . . 
	if fType == "rig":
		if cmds.objExists("*RIGDATA"):
			rigDataStuff = cmds.ls("*RIGDATA")
			cmds.delete("*RIGDATA")

		# put all ctrls into ALLKEYABLE
		cFuncs.crvsToAllkeyable()
		print "putting all crvs under god node into allkeyable set"

#again generically to both rig and geo
	#optimize scene

##########  rather . . . have one big master asset window that sets off the above processes

# def masterGeoUI(asset, assetFolder, fType, *args):

# 	if cmds.window("mstrGeoWin", exists = True):
# 		cmds.deleteUI("mstrGeoWin")

# 	mgWidget["win"] = cmds.window("mstrGeoWin", t="Master Geo Workshop", w=100, h=120)
# 	mgWidget["mainCLO"] = cmds.columnLayout(w=100, h=120)

# 	mgWidget["masterButton"] = cmds.button(l="Master Asset", w=100, h=40, c=partial(masterGeo, asset, assetFolder, "geo"))
# 	mgWidget["cancelButton"] = cmds.button(l="Cancel", w=100, h=40)
# 	mgWidget["pushButton"] = cmds.button(l="Push Through Rigging", w=100, h=40)	

# 	cmds.showWindow(mgWidget["win"])

def masterShot():
	pass
	#mmight not need to have breakout funcs from here for lgt, anm, fx, etc. . . 

#args should be asset, assetFolder, fType

def masterAssetUI(asset, assetFolder, fType, *args):
	if cmds.window("mstWin", exists = True):
		cmds.deleteUI("mstWin")
		
	mWidgets["win"] = cmds.window("mstWin", w=300, h=100, t="Master Window")
	
	mWidgets["mainCLO"] = cmds.columnLayout(w=300, h=100)
	cmds.text(l=asset)
	cmds.text(l=assetFolder)
	cmds.text(l=fType)
	
	#options to freeze geo, if fType == "geo" then give option NOT to master through. . . 
	
	mWidgets["mstBut"] = cmds.button(l = "Master", w=300, h=30, bgc = (.5, .9, .5))
	
	cmds.showWindow(mWidgets["win"])