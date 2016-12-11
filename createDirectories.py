# createDirectories.py
import maya.cmds as cmds

import os, sys
from functools import partial
import chrlx_pipe.chrlxFuncs as cFuncs
###########
# this module is used to create directories for new shots, assets, etc
# createAssDirs() is what we'd call externally to create a director structure for new asset
#
############

widgets = {}

def createAssetUI(proj, assFolder, *args):

	if cmds.window("createAssWin", exists = True):
		cmds.deleteUI("createAssWin")

	widgets["createAssWin"] = cmds.window("createAssWin", t="Create New Asset", s=False)
	widgets["mainCLO"] = cmds.columnLayout()

	widgets["mainFLO"] = cmds.formLayout(w = 300, h=120, bgc = (.3,.3,.3))

	widgets["name"] = cmds.textFieldGrp(l="Asset Name: ", w=300, cw = [(1, 70), (2,220)], cal = [(1,"left"), (2, "left")])
	widgets["type"] = cmds.radioButtonGrp(l="Type: ", labelArray3 = ("Char", "Prop", "Set"), numberOfRadioButtons = 3, sl=1, cal = [(1, "left"), (2,"left"), (3, "left"), (4, "left")], cw=[(1, 70), (2, 50), (3,50), (4,50)])
	widgets["createBut"] = cmds.button(l="Create Asset!", w=300, h=50, bgc = (.5, .8, .5), c=partial(createWinAssetDirs, proj, assFolder))

	cmds.formLayout(widgets["mainFLO"], e=True, af = [
		(widgets["name"], "left", 0), 
		(widgets["name"], "top", 10),
		(widgets["type"], "left", 0), 
		(widgets["type"], "top", 40),
		(widgets["createBut"], "left", 0), 
		(widgets["createBut"], "top", 70)])

	cmds.window(widgets["createAssWin"], e=True, w=300, h=120)
	cmds.showWindow(widgets["createAssWin"])

def createWinAssetDirs(proj, folder, *args):
	"""folder is the component folder (asset folder). Proj is project folder"""

	name = cmds.textFieldGrp(widgets["name"], q=True, tx=True)
	type = cmds.radioButtonGrp(widgets["type"], q=True, sl=True)

	#here we compare that list of assets with our proposed name
	assets = cFuncs.getSpotAssetList(folder)
	if name in assets:
		cmds.confirmDialog(t="Name Exists!", m = "There is already an asset of this name\nin this project! Please enter another.")
		return()

	if type == 1:
		assType = "characters"
	elif type == 2:
		assType = "props"
	elif type == 3:
		assType = "sets"

	createAssDirs(folder, assType, name)
	
	if cmds.window("assetWin", exists=True):
		import chrlx_pipe.assetWin as assWin
		assWin.populateAssets(proj)

def createAssDirs(assetFolder, assType, name):
	"""creates asset directories from args
		-asset folder is path to asset folder under 3D
		-assType is either "characters", "props", or "sets"
		-name is string name of the new character
	"""

	#do this again (like above) just to make sure we don't repeat a name if we're calling externally
	assetFolder = "{0}/{1}/{2}".format(assetFolder, assType, name)
	if not os.path.isdir(assetFolder):
		print "------making {}".format(assetFolder)
		os.makedirs(assetFolder)
		assetContents = ["geo", "rig", "mtl", "sourceImages", "reference", "icon"]
		for direct in assetContents:
			assDirect = "{0}/{1}".format(assetFolder, direct)
			print "------making {}".format(assDirect)
			os.makedirs(assDirect)
		geoContents = ["import_export", "past_versions", "workshops"]
		for direct in geoContents:
			geoDirect = "{0}/geo/{1}".format(assetFolder, direct)
			print "------making {}".format(geoDirect)
			os.makedirs(geoDirect)
		geoWSContents = ["max", "mudbox", "zbrush"]
		for direct in geoWSContents:
			WSDirect = "{0}/geo/workshops/{1}".format(assetFolder, direct)
			print "------making {}".format(WSDirect)
			os.makedirs(WSDirect)
		rigContents = ["import_export", "past_versions", "workshops"]
		for direct in rigContents:
			rigDirect = "{0}/rig/{1}".format(assetFolder, direct)
			print "------making {}".format(rigDirect)
			os.makedirs(rigDirect)
		mtlContents = ["import_export", "past_versions", "workshops"]
		for direct in mtlContents:
			mtlDirect = "{0}/mtl/{1}".format(assetFolder, direct)
			os.makedirs(mtlDirect)


		if cmds.window("createAssWin", exists = True):
			cmds.deleteUI("createAssWin")
	else:
		cmds.warning("That directory already exists!")
		###### - - - - - return this as a list

def createAsset(proj, assFolder, *args):
	"""proj - is the path """
	createAssetUI(proj, assFolder)