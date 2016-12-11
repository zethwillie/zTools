import maya.cmds as cmds
import maya.mel as mel
from chrlx import utils

import os, fnmatch, shutil, sys, fileinput

###################################################
# helper scripts that do little functions for the pipeline
# wherever possible, these should be generic (call/return from external scripts or manually)
#####################################################

cJobPaths = {
	"charPath":"assets/characters",
	"propPath":"assets/props",
	"setPath":"assets/sets",
	"shotPath":"scenes"
	}


def fixPath(path, *args):
	"""cleans up the path for use in both win and linux. Remember to pass handmade paths as r'string'. """
	
	if path:
		cleanPath = path.replace("\\", "/")
		return cleanPath
	else:
		return Null

def getCurrentProject(*args):
	"""returns the current project path"""

	proj = cmds.workspace(q=True, act=True)
	if proj:
		cleanProj = fixPath(proj)
		return cleanProj
	else: 
		print "chrlxFuncs: couldn't find a valid project"
		return proj

def setProject(path, *args):
	"""given a path, this will set the project to the path
	---needs a bit more error checking and cleaner way to deal with win vs linux paths
	"""
	#clean up the path for linux and win
	fixedPath = fixPath(path)
	#if the dir exists, then set the project to that
	############
	#check where to set up the render directories, caches, files, etc bc they won't be in the default locations
	#maybe a separate script for that
	############
	if os.path.isdir(fixedPath):
		mel.eval('setProject "{}";'.format(fixedPath))
		ws = cmds.workspace(q=True, fn=True)
		cmds.warning("You've set the the current project to: %s"%(ws))
	else:
		cmds.warning("chrlxFuncs.setProject(): I can't find: {}. talk to a TD!".format(fixedPath))

def getProjectAssetList(job, *args):
	"""returns a list of lists (chars, props, sets), given a job path"""
	cJob = fixPath(job)
	chars = []
	props = []
	sets = []

	charRoot = "{0}/{1}".format(cJob, cJobPaths["charPath"])
	propRoot = "{0}/{1}".format(cJob, cJobPaths["propPath"])
	setRoot = "{0}/{1}".format(cJob, cJobPaths["setPath"])
	dirs = [charRoot, propRoot, setRoot]
	#check if the dir exists
	for dir in dirs:
		exists = os.path.isdir(dir)
		if exists:
			try:
				if dir==charRoot:
					chars = os.listdir(dir)
					chars.sort()
					chars = [x for x in chars if (x[0] != "." and x != "archive")]
				elif dir==propRoot:
					props = os.listdir(dir)
					props.sort()
					props = [x for x in props if (x[0] != "." and x != "archive")]
				elif dir==setRoot:
					sets = os.listdir(dir)
					sets.sort()
					sets = [x for x in sets if (x[0] != "." and x != "archive")]					
			except:
				cmds.warning("chrlxFuncs.getProjectAssetList: couldn't access {}".format(dir))		
		else:
			cmds.warning("chrlxFuncs.getProjectAssetList: Couldn't find the {} path! Skipping.".format(dir))
	
	return chars, props, sets

def getProjectShotList(job, *args):
	"""given a job(spot) path, returns the list of folders in the shot path of that job"""

	cJob = fixPath(job)
	shotRoot = os.path.join(cJob, cJobPaths["shotPath"])
	try:
		shots = os.listdir(shotRoot)
		#clear out files
		for shot in shots:
			good = os.path.isdir("%s/%s"%(shotRoot, shot))
			if not good:
				shots.remove(shot)
		return shots
	except:
		cmds.warning("chrlxFuncs.getProjectShotList: No directory!!")

def referenceIn(scene, prefix, *args):
	"""reference scenes, no namespace and will replace the obj name with the prefix arg"""
	
	#############
	#---- need to check names in scene, increment if necessary
	#

	path = fixPath(scene)
	newPath = path.replace("\\", "/")
	ref = cmds.file(path, reference= True, uns = False, rpr = prefix)
	#maybe use parameter to push out a list of all the new nodes? 
	return ref

def removeReference(node, *args):
	cmds.file(removeReference=True, referenceNode = refNode)
	#look through ALLKEYABLE -find ref objs that line up 

def makeDirectory(path, *args):
	"""just makes a directory in the path if one doesn't exists"""

	cPath = fixPath(path) #cleans the path if we're hand typing it
	#check if the dir exists already
	exists = os.path.isdir(path)
	if not exists:
		try:
			os.makedirs(cPath)
			cmds.warning("Just made directory: {}".format(cPath))
		except:
			cmds.warning("chrlxFuncs.makeDirectory: Couldn't make: {0}. Error Type: {1}".format(sys.exc_info()[0]))

def getAssetMaster(asset, assetPath, fType, *args):
	"""takes the asset name and path to the geo, rig file and returns the path the master, return null if not there"""
	
	maya = "{0}_{1}.ma".format(asset, fType)
	if (maya in os.listdir("{0}/{1}".format(assetPath, fType))):
		return("{0}/{1}/{2}".format(assetPath, fType, maya))
	else:
		return None

def getLatestAssetWS(asset, assetPath, fType, *args):
	"""given an asset base name, asset base directory, and type ("rig" or "geo"), find the latest version of the WS in that dir, returns the full path to file
	asset_[type].ma.v#
	get all file in dir, and filter them for only asset_type.ma.v#
	"""
############- -- - - check if this is/has a directory (I'm getting an OS error)
	ws = fnmatch.filter(os.listdir("{0}/{1}/workshops".format(assetPath, fType)), "{0}_{1}_ws_v[0-9]*.ma".format(asset, fType))
	
	#find the highest number WS
	sortNum = 0
	sortWS = "" #the file name of the last workshop file
	try:
		for x in range(0, len(ws)):
			#strip off the .ma, then get things after "_v". note this breaks if not named correctly!
			num = int(ws[x].rpartition("_v")[2].rstrip(".ma"))
			if num > sortNum:
				sortNum = num
				sortWS = ws[x]
	except:
		pass
		
	if sortWS:
		return "{0}/{1}/workshops/{2}".format(assetPath, fType, sortWS)
	else: 
		return None
		print "found no workshop files for {}".format(asset)

def getLatestShotWS(shot, shotPath, fType ,*args):
	"""given a directory, asset base name and type ("lgt", "anm", "fx"), find the latest version of the WS in that dir, returns the path to file"""

############ - -- - - check if it's shot, dev, previs, etc? ? ? 

############- -- - - check if this is/has a directory (I'm getting an OS error)
	ws = fnmatch.filter(os.listdir("{}/workshops".format(shotPath)), "{0}_{1}_ws_v[0-9]*.ma".format(asset, fType))
	
	#find the highest number WS
	sortNum = 0
	sortWS = "" #the file name of the last workshop file
	try:
		for x in range(0, len(ws)):
			#strip off the .ma, then get things after "_v". note this breaks if not named correctly!
			num = int(ws[x].rpartition("_v")[2].rstrip(".ma"))
			if num > sortNum:
				sortNum = num
				sortWS = ws[x]
	except:
		pass
		
	if sortWS:
		return "{0}/workshop/{1}".format(shotPath,sortWS)
	else: 
		return None
		print "found no workshop files for {}".format(asset)

def checkCurrentWSMatch(selectedAsset, fType, *args):
	"""checks that the selected asset from win is actually the asset of the open scene. Puts up confirm dialog telling user this and returns 'cancel' if person decides not to continue"""
	result = ""

	#get asset from current open ws scene name
	current = os.path.basename(cmds.file(q=True, sceneName = True))
	test = "{0}_{1}_ws".format(selectedAsset, fType)
	#strip off "_v###.ma" from open scene
	if current[:-8] != test:
		result = cmds.confirmDialog(t="Workshop Name Mismatch!", m = "Current scene: {0}\n\nSelected asset: {1}\n\nYou are attempting to save this to the {2} {3} folder!".format(current, test, selectedAsset, fType), b = ("Continue", "Cancel"), db = "Continue", cb = "Cancel", ds = "Cancel", bgc = (.8, .6, .6))
	return result

def checkCurrentMasterMatch(asset, fType, *args):
	"""just a boolean to check whether the current scene's name lines up with the workshop format for the selected asset (in order to master)"""

	check = False
	currentScenePath = cmds.file(q=True, sceneName=True) #gets the full path
	currentScene = os.path.basename(currentScenePath)[:-8]
	wsFormat = "{0}_{1}_ws".format(asset, fType)
	print "chrlxFuncs.checkCurrentMasterMatch: \ncurrentScene = {0}\nwsFormat = {1}".format(currentScene, wsFormat)
	if currentScene == wsFormat:
		check = True
	return(check)

def incrementWS(asset, assetPath, fType, *args):
	"""takes in the workshop path as filepath (incl file) 
		filePath is full path to the workshop file
		asset is asset or shot name (i.e. "man")
		assetPath is main asset or shot folder (ie. . . .spot/3D/assets/chars/man)
		fType is "geo", "rig", "anm", "lgt", "fx"
		- returns the full path to the new increment
	"""
	if fType == "geo" or fType == "rig":
		latestWsPath = getLatestAssetWS(asset, assetPath, fType)

	if fType == "lgt" or fType == "fx" or fType == "anm":
		latestWsPath = getLatestShotWS(asset, assetPath, fType)

	#if filePath = None, then create a first path for newFile
	if latestWsPath:
		folder, doc = os.path.split(latestWsPath)
		num = int(doc.rpartition("_v")[2].rstrip(".ma"))

		base = doc.rpartition("v")[0]
		incr = num + 1
		newDoc = base + "v{:0>3d}".format(incr)
		newFile = "{0}/{1}".format(folder, newDoc)

	else:
		wsFile = "{0}_{1}_ws_v001".format(asset, fType)
		newFile = "{0}/{1}/workshops/{2}".format(assetPath, fType, wsFile)
	return newFile

def getLastAssetMasterVersion(asset, assetPath, fType, *args):
	"""given an asset base name and the master version folder path, return the latest master version file path"""

	if asset and assetPath and fType:

		ws = fnmatch.filter(os.listdir("{0}/{1}/past_versions".format(assetPath, fType)), "{0}_{1}_v[0-9]*.ma".format(asset, fType))
		
		#find the highest number WS
		sortNum = 0
		sortWS = "" #the file name of the last workshop file
		try:
			for x in range(0, len(ws)):
				#strip off the .ma, then get things after "_v". note this breaks if not named correctly!
				num = int(ws[x].rpartition("_v")[2].rstrip(".ma"))
				if num > sortNum:
					sortNum = num
					sortWS = ws[x]
		except:
			pass
			
		if sortWS:
			return "{0}/past_versions/{1}".format(assetPath,sortWS)
		else: 
			return None

	else:
		cmds.warning("chrlxFuncs.getLastAssetMasterVersion: you haven't given me all the args I need")
		return "Abort"



def getShotMaster(shot, path, *args):
	"""check whether theres an anm file and returns path"""

	pass
	# mayaF = "%s_anm.ma"%shot
	# if (mayaF in os.listdir(path)):
	# 	return("%s/%s"%(path, mayaF))
	# else:
	# 	return None

def getJobNumber(jobName, *args):
	"""just pulls the 6 digit job number itself out of the charlex job name"""
	jobNum = jobName.rpartition("_")[2]
	if len(jobNum) == 6:
		return(jobNum)
	else:
		return("")

def getShotNumber(shot, *args):
	"""just pulls out the shot number as a three digit int from the shot name"""
	
	num = shot.lstrip("shot")
	if len(num)== 3:
		return num
	else:
		return ""

def createAssetIcon(refPath, asset, *args):
	"""takes the char reference folder path and asset name, playblasts a frame and renames it correctly (PNG format)"""
	#Get directory and asset name
	fname = "{0}/{1}".format(refPath, asset)

	im = cmds.playblast(filename = fname, forceOverwrite = 1, orn = 0, fmt = "image", frame = cmds.currentTime(q=True), fp=4, v=0, c="png", wh=(154,154), p=100)

	# # now strip the padding
	nums = im.replace(".####", ".0000")
	base = im.rpartition(".####")
	os.rename(nums, base[0] + "Icon" + base[2]) 
	
def openFolderInExplorer(path, *args):
	"""takes in path and opens it in os folder"""
	import subprocess

	if sys.platform == "win32":
		import webbrowser as browser
		winPath = fixPath(path)
		# text = 'explorer "{0}"'.format(path)
		# subprocess.Popen(text)
		win = path.replace("/", "\\")
		os.startfile(win)
	elif sys.platform == "darwin":
		pass
	elif sys.platform == "linux" or sys.platform=="linux2":
		linPath = fixPath(path)
		subprocess.Popen(['xdg-open', linPath])

def moveFolder(source, target, *args):
	"""moves a folder and contents to new location"""
	#get asset folder 
	# use shutil.copytree(src, dst)
	if source and target:

		#####  test if the desitnation folder already exists, flash option to overwrite? 
		# shutil.copytree(source, target)
		shutil.move(source, target)

		return "Moved - asset: \n{0}\nTo - Destination:\n{1}".format(source, target)
	else: 
		return "chrlxFuncs.moveFolder: wasn't given two paths to move"

		if cmds.window("assetWin", exists=True):
			import chrlxPipe.assetWin as assWin
			assWin.populateWindow(asset)

def getLightList(*args):
	"""returns all lights in the scene"""

	lgtShp = cmds.ls(type="light")
	lights = []

	if lgtShp:
		for shp in lgtShp:
			obj = cmds.listRelatives(shp, p=True)[0]
			lights.append(obj)

	return lights

def getCamList(*args):
	"""returns all cams (not default) in scene"""

	camShps = cmds.ls(type="camera")
	cams = []
	camList = ["front", "persp", "side", "top"]
	
	if camShps:
		for cam in camShps:
			obj = cmds.listRelatives(cam, p=True)[0]
			if obj not in camList:
				cams.append(obj)
			
	return cams

def removeNamespace(*args):
	"""looks in the current scene and removes namespaces"""
	rem = ["UI", "shared"]
	ns = cmds.namespaceInfo(lon=True, r=True)
	for y in rem:
		ns.remove(y)
	ns.sort(key = lambda a: a.count(":"), reverse=True)
	for n in ns:
		ps = cmds.ls("{}:*".format(n), type="transform")
		for p in ps:
			cmds.rename(p, p.rpartition(":")[2]) 
		cmds.namespace(rm=n)
	return(ns)

def mstCtrlTemplate(*args):
	"""creates a master control template object for geo scenes"""
	mstCtrl = cmds.curve(n="ctrlSizeTemplateCrv", d=1, p=[[0.045038530330620184, 0.25951525008201387, -5.210460506620644], [1.3936049431985766, 0.2595152500820137, -5.032918370204105], [2.650268783640949, 0.2595152500820139, -4.512391164149015], [3.7293904876667763, 0.25951525008201365, -3.684351957336151], [4.557429694479641, 0.25951525008201354, -2.60523025331032], [5.077956900534729, 0.25951525008201354, -1.3485664128679486], [5.255499036951263, 0.25951525008201354, 3.832412260469572e-15], [5.077956900534727, 0.2595152500820132, 1.348566412867956], [4.5574296944796355, 0.25951525008201354, 2.605230253310326], [3.729390487666771, 0.25951525008201337, 3.6843519573361547], [2.650268783640938, 0.2595152500820134, 4.512391164149018], [1.3936049431985678, 0.2595152500820136, 5.032918370204106], [0.04503853033061642, 0.2595152500820139, 5.210460506620647], [-1.3035278825373362, 0.259515250082014, 5.032918370204104], [-2.560191722979707, 0.2595152500820138, 4.512391164149014], [-3.639313427005534, 0.2595152500820142, 3.684351957336151], [-4.467352633818398, 0.2595152500820135, 2.6052302533103218], [-4.987879839873487, 0.2595152500820144, 1.3485664128679502], [-5.165421976290027, 0.25951525008201404, -1.5546578037753924e-15], [-4.987879839873485, 0.2595152500820145, -1.3485664128679529], [-4.467352633818397, 0.25951525008201376, -2.6052302533103235], [-3.6393134270055336, 0.25951525008201437, -3.6843519573361525], [-2.5601917229797033, 0.25951525008201387, -4.512391164149015], [-1.3035278825373326, 0.259515250082014, -5.032918370204103], [0.045038530330620184, 0.25951525008201387, -5.210460506620644], [0.04503853033061907, -0.25951525008201276, -5.210460506620644], [1.3936049431985753, -0.2595152500820128, -5.032918370204105], [2.6502687836409473, -0.2595152500820128, -4.512391164149015], [3.7293904876667785, -0.2595152500820133, -3.684351957336151], [4.55742969447964, -0.25951525008201276, -2.60523025331032], [5.07795690053473, -0.2595152500820132, -1.3485664128679486], [5.255499036951268, -0.2595152500820131, 3.832412260469572e-15], [5.255499036951263, 0.25951525008201354, 3.832412260469572e-15], [5.255499036951268, -0.2595152500820131, 3.832412260469572e-15], [5.077956900534729, -0.25951525008201354, 1.348566412867956], [4.5574296944796355, -0.259515250082013, 2.605230253310326], [3.7293904876667727, -0.25951525008201326, 3.6843519573361547], [2.6502687836409393, -0.2595152500820128, 4.512391164149018], [1.3936049431985689, -0.25951525008201337, 5.032918370204106], [0.04503853033061624, -0.25951525008201304, 5.210460506620647], [0.04503853033061642, 0.2595152500820139, 5.210460506620647], [0.04503853033061624, -0.25951525008201304, 5.210460506620647], [-1.3035278825373373, -0.259515250082013, 5.032918370204104], [-2.560191722979707, -0.25951525008201276, 4.512391164149014], [-3.639313427005533, -0.2595152500820126, 3.684351957336151], [-4.467352633818397, -0.2595152500820125, 2.6052302533103218], [-4.987879839873487, -0.2595152500820122, 1.3485664128679502], [-5.165421976290028, -0.25951525008201276, -1.5546578037753924e-15], [-5.165421976290027, 0.25951525008201404, -1.5546578037753924e-15], [-5.165421976290028, -0.25951525008201276, -1.5546578037753924e-15], [-4.987879839873485, -0.25951525008201226, -1.3485664128679529], [-4.467352633818397, -0.2595152500820125, -2.6052302533103235], [-3.639313427005532, -0.2595152500820127, -3.6843519573361525], [-2.560191722979703, -0.25951525008201204, -4.512391164149015], [-1.303527882537332, -0.2595152500820125, -5.032918370204103], [0.04503853033061907, -0.25951525008201276, -5.210460506620644]])
	cmds.rename(cmds.listRelatives(mstCtrl, s=True)[0], "{}Shape".format(mstCtrl))
	cmds.select(clear=True)
	
	for a in ["tx", "ty", "tz", "rx", "ry", "rz"]:
		cmds.setAttr("{0}.{1}".format(mstCtrl, a), k=False)
	cmds.setAttr("{}.overrideEnabled".format(mstCtrl), 1)
	cmds.setAttr("{}.overrideColor".format(mstCtrl), 13)

def putFileInfo(fType = "", wsNum = 000, note = "", *args):
	"""given args, will modify the open scene's file info:
		info keys that will change: 'FILETYPE', 'USER', 'WORKSHOP', 'DATE', 'CHARLX_NOTE'
		args are:
		-fType (should be "geo", "rig", "lgt", "anm", "fx", ["mtl"?])
		-[user will get info from open scene]
		-workshop num (###)
		-[date will get from open scene]
		-note (some text string)
	"""
	user = mel.eval("getenv USER")
	date = cmds.date()

	cmds.fileInfo("FILETYPE", fType)
	cmds.fileInfo("USER", user)
	cmds.fileInfo("WORKSHOP", wsNum)
	cmds.fileInfo("DATE", date)
	cmds.fileInfo("CHRLX_NOTE", note)

def projectCheck():
	"""if project is the correct schema (via chrlx.utils), then return to func, else throw error"""
	proj = getCurrentProject()
	pm = utils.PathManager(proj)
	check = pm.spotSchema

	if check == 2:
		return("good")
	else:
		return(None)

def crvsToAllkeyable(mst=None):
	"""for rig mastering. This will put all crvs under the master into all keyable set"""
	if not mst:
		mst = "GOD"
	if cmds.objExists(mst):
		children = cmds.listRelatives(mst, ad=True, s=False)
		crvs = []
		if children:
			for chld in children:
				if cmds.objectType(chld) == "transform":
					shp = cmds.listRelatives(chld, s=True)
					if shp and cmds.objectType(shp[0]) == "nurbsCurve":
						crvs.append(chld)

		for crv in crvs:   
			cmds.sets(crv, e=True, fe="ALLKEYABLE" )

def getSpotAssetList(assFolder):
	"""return list of all assets in a spot folder (incl arched assets). NOT paths, just asset names
		-assFolder is the assetFolder under 3D in a spot folder
	"""

	if assFolder:
		assets = []
		types = ["characters", "props", "sets"]
		for assType in types:
			assTypeFolder = "{0}/{1}".format(assFolder, assType)
			comps = os.listdir(assTypeFolder)
			comps.remove("archive")
			for comp in comps:
				assets.append(comp)
			archiveFolder = "{}/archive".format(assTypeFolder)
			archs = os.listdir(archiveFolder)
			for arch in archs:
				assets.append(arch)
		return(assets)
	else:
		return(None)

def getFilesInPath(path):
	"""returns a list of files only in a path"""
	files = []
	for obj in os.listdir(path):
		if os.path.isfile(os.path.join(path, obj)):
			files.append(fixPath(os.path.join(path, obj)))

	return files

def replaceTextInFile(filePath, searchTxt, replaceTxt):
	"""opens the file and replaces [searchTxt] with [replaceTxt] in place in the file"""

	fileData = None
	with open(filePath, "r") as file:
		fileData = file.read()
		
	fileData = fileData.replace(searchTxt, replaceTxt)
	
	with open(filePath, "w") as file:
		file.write(fileData)
