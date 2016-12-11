import os
import maya.cmds as cmds
from functools import partial
from shutil import copyfile
from chrlx.utils import PathManager
import chrlx_pipe.projectSetter as projSet
from chrlx_pipe.createDirectories import createAssDirs
import chrlx_pipe.chrlxFuncs as cFuncs


widgets = {}
newProjPathSelect = ""

def duplicateAssetUI(oldAss = None, *args):
	if cmds.window("dupeWin", exists=True):
		cmds.deleteUI("dupeWin")
	widgets["win"] = cmds.window("dupeWin", w=400, h=200, t="Duplicate Asset")
	widgets["mainCLO"] = cmds.columnLayout(w=400, h=200)

	cmds.text(l="Select either existing asset path OR asset file (asset win will autopopulate)")
	widgets["oldTFBG"] = cmds.textFieldButtonGrp(l="Old Asset Path:", fi= oldAss, buttonLabel="<<<", cal =[(1, "left"), (2,"left"), (3, "left")], cw=[(1, 125), (2, 235), (3,40)], bc=partial(getPath, "oldTFBG"))
	cmds.text(l="---------------------------------------------------------------------------------------------------", h=20)
	widgets["nameTFG"] = cmds.textFieldGrp(l="New Asset Name:", cal=[(1, "left"), (2, "left")], cw=[(1, 125), (2, 200)])
	widgets["assTypeRBG"] = cmds.radioButtonGrp(l="Asset Type:", labelArray3 = ("Char", "Prop", "Set"), numberOfRadioButtons = 3, sl=1, cal = [(1, "left"), (2,"left"), (3, "left"), (4, "left")], cw=[(1, 70), (2, 50), (3,50), (4,50)])
	cmds.text(l="Select new asset folder (the asset folder under 3D)")
	widgets["newTFBG"] = cmds.textFieldButtonGrp(l="New Asset Project Path:", bl="<<<", cal =[(1, "left"), (2,"left"), (3, "left")], cw=[(1, 125), (2, 235), (3,40)], bc = projectSelectUI)
	cmds.separator(h=20)
	widgets["dupeBut"] = cmds.button(l="Duplicate Asset", w=400, h=50, bgc=(.5, .8, .5), c=readWinDupe)


	cmds.window(widgets["win"], e=True, w=400, h=200)
	cmds.showWindow(widgets["win"])

def getPath(pathField, *args):
	"""gets the path that will fill the field group"""
	path = cmds.fileDialog2(fm=2)
	cmds.textFieldButtonGrp(widgets[pathField], e=True, fi=path[0])
	val = cmds.textFieldButtonGrp(widgets["oldTFBG"], q=True, tx=True)

	sel = cmds.radioButtonGrp(widgets["assTypeRBG"], q=True, sl=True)

	if not cmds.textFieldButtonGrp(widgets["newTFBG"], q=True, tx=True):
		if val:
			oldPath = PathManager(path[0])
			if sel == 1:
				newDest = os.path.join(oldPath.charPath)
			if sel == 2:
				newDest = os.path.join(oldPath.propPath)
			if sel == 3:
				newDest = os.path.join(os.path.join(oldPath.assetPath, "sets"))								
			
			cmds.textFieldButtonGrp(widgets["newTFBG"], e=True, fi=newDest)

def readWinDupe(*args):
	"""gets the info from the win and passes it to dupe execute"""
	oldAss = cmds.textFieldButtonGrp(widgets["oldTFBG"], q=True, tx=True)
	newAssBase = cmds.textFieldButtonGrp(widgets["newTFBG"], q=True, tx=True)

	if cmds.window("dupeWin", exists=True):
		newType = cmds.radioButtonGrp(widgets["assTypeRBG"], q=True, sl=True)
		if newType ==1 :
			newType = "characters"
		if newType == 2:
			newType = "props"
		if newType == 3:
			newType = "sets"
	name = cmds.textFieldGrp(widgets["nameTFG"], q=True, tx=True)
	newAss = os.path.join(newAssBase, name)
	if oldAss and newAssBase and name:
		duplicateExecute(oldAss, newAss, newType)
	else:
		cmds.warning("You have to fill in all of the fields!")

def duplicateExecute(oldAss=None, newAss=None, newType=None, *args):
	"""given an old asset name (full path, [. . ./3d/assets/TYPE/NAME]) and a new asset name (...3d/assets/TYPE/NAME), newType is either [characters, props or sets]"""
	
	#create objs that we can get info from the utils function
	oldAss = cFuncs.fixPath(oldAss)
	newAssRaw = cFuncs.fixPath(newAss)
	#replace type with newType
	newAss = cFuncs.fixPath(os.path.join(os.path.join(os.path.dirname(os.path.dirname(newAssRaw)), newType), os.path.basename(newAss)))
	oldAssNew = cFuncs.fixPath(os.path.join(os.path.join(os.path.dirname(os.path.dirname(oldAss)), newType), os.path.basename(oldAss)))
	print "oldAssNew:", oldAssNew

	oldPath = PathManager(oldAss)
	newPath = PathManager(newAss)

	oldAssName = os.path.basename(oldAss)
	newAssName = os.path.basename(newAss)

	# print "oldassname:", oldAssName
	# print "newAssName:", newAssName
	#create an asset structure for the new name
	createAssDirs(newPath.assetPath, newType, newAssName)
	
	#geo latest ws - rename, replace references
	oldGeoWS = cFuncs.getLatestAssetWS(oldAssName, oldAss, "geo")
	newGeoWS = ""
	if oldGeoWS:
		newGeoWS = "{0}/geo/workshops/{1}".format(newAss, os.path.basename(oldGeoWS).replace(oldAssName.partition("_")[0], newAssName))
		print newGeoWS
		copyfile(oldGeoWS, newGeoWS)

	#geo master if exists - rename 
	oldGeoMst = cFuncs.getAssetMaster(oldAssName, oldAss, "geo")
	newGeoMst = ""
	if oldGeoMst:
		newGeoMst = "{0}/geo/{1}".format(newAss, os.path.basename(oldGeoMst).replace(oldAssName.partition("_")[0], newAssName))
		copyfile(oldGeoMst, newGeoMst)

	#rig latest ws if exists - rename, replace references
	oldRigWS = cFuncs.getLatestAssetWS(oldAssName, oldAss, "rig")
	newRigWS = ""
	if oldRigWS:
		newRigWS = "{0}/rig/workshops/{1}".format(newAss, os.path.basename(oldRigWS).replace(oldAssName.partition("_")[0], newAssName))
		copyfile(oldRigWS, newRigWS)
	
	#get rig master and copy
	oldRigMst = cFuncs.getAssetMaster(oldAssName, oldAss, "rig")
	newRigMst = ""
	if oldRigMst:
		newRigMst = "{0}/rig/{1}".format(newAss, os.path.basename(oldRigMst).replace(oldAssName.partition("_")[0], newAssName))
		copyfile(oldRigMst, newRigMst)

######## copy mtl and shader files. . . . 

	replaceFiles = []
	# copy contents of source images
	for fl in cFuncs.getFilesInPath(os.path.join(oldAss, "sourceImages")):
		if fl:
			copyfile(fl, "{0}/sourceImages/{1}".format(newAss, os.path.basename(fl).replace(oldAssName, newAssName)))
			#replaceFiles.append(fl)

	############ - now we have to find the refs to the geoWS folder and replace it with the new one, same with source images in all files
	# files to search for: oldGeoMst, sourceImage list
	#replaceFiles.append(oldGeoMst)
	
########## -- add mtl file to this . . .
	filesToSearch = [newRigWS]

	for doc in filesToSearch:
		cFuncs.replaceTextInFile(doc, oldGeoMst, newGeoMst)

	if cmds.window("dupeWin", exists=True):
		cmds.deleteUI("dupeWin")

def projectSelectUI(*args):
	sel = cmds.radioButtonGrp(widgets["assTypeRBG"], q=True, sl=True)
	if sel == 1:
		assType = "characters"
	if sel == 2:
		assType = "props"
	if sel == 3:
		assType = "sets"
################ -------- do this better
	proj = projSet.projectSetter("dupe", widgets["newTFBG"], assType)

def duplicateAsset(oldAss, *args):
	"""oldAss = the path the specific asset folder (ie. ...3d/assets/characters/CHARNAME)"""
	if oldAss:
		duplicateAssetUI(oldAss)
	else:
		cmds.warning("No asset selected to dupe!")