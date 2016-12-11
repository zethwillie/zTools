#unarchiveAssets.py

import maya.cmds as cmds
import os, sys

import chrlx_pipe.chrlxFuncs as cFuncs

widgets = {}
archFolders = []
assFolders = []
currentProj = ""

def unarchiveUI(*args):
	if cmds.window("unarchWin", exists = True):
		cmds.deleteUI("unarchWin")

	widgets["win"] = cmds.window("unarchWin", t = "Archived Assets to Restore", s=False)
	widgets["mainCLO"] = cmds.columnLayout(w=550, h=300)

	widgets["mainFLO"] = cmds.formLayout(w=550, h=300)
	widgets["charTSL"] = cmds.textScrollList(w=170, h=200, allowMultiSelection = True)
	widgets["propTSL"] = cmds.textScrollList(w=170, h=200, allowMultiSelection = True)
	widgets["setTSL"] = cmds.textScrollList(w=170, h=200, allowMultiSelection = True)

	widgets["charText"] = cmds.text(l="Characters")
	widgets["propText"] = cmds.text(l="Props")
	widgets["setText"] = cmds.text(l="Sets")

	widgets["unarchBut"] = cmds.button(l="Unarchive selected Assets", w= 530, h=50, bgc = (.5, .8,.5), c=restoreAssets)

	cmds.formLayout(widgets["mainFLO"], e=True, af=
		[(widgets["charTSL"], "top", 20),
		(widgets["charTSL"], "left", 10), 
		(widgets["propTSL"], "top", 20),
		(widgets["propTSL"], "left", 190),
		(widgets["setTSL"], "top", 20),
		(widgets["setTSL"], "left", 370),
		(widgets["charText"], "left", 50),
		(widgets["charText"], "top", 5),
		(widgets["propText"], "left", 260),
		(widgets["propText"], "top", 5),	
		(widgets["setText"], "left", 440),
		(widgets["setText"], "top", 5),
		(widgets["unarchBut"], "left", 10),
		(widgets["unarchBut"], "top", 230), 		 
		])

	cmds.window(widgets["win"], e=True, w=550, h=300)
	cmds.showWindow(widgets["win"])

	populateWindow()

def populateWindow(*args):
	cmds.textScrollList(widgets["charTSL"], e=True, removeAll = True)
	cmds.textScrollList(widgets["propTSL"], e=True, removeAll = True)
	cmds.textScrollList(widgets["setTSL"], e=True, removeAll = True)

	archChars = os.listdir(archFolders[0])
	archProps = os.listdir(archFolders[1])
	archSets = os.listdir(archFolders[2])

	cmds.textScrollList(widgets["charTSL"], e=True, a=archChars)
	cmds.textScrollList(widgets["propTSL"], e=True, a=archProps)
	cmds.textScrollList(widgets["setTSL"], e=True, a=archSets)

def restoreAssets(*args):
	restoreChars = cmds.textScrollList(widgets["charTSL"], q=True, si=True)
	restoreProps = cmds.textScrollList(widgets["propTSL"], q=True, si=True)
	restoreSets = cmds.textScrollList(widgets["setTSL"], q=True, si=True)

	restoreAsses = [restoreChars, restoreProps, restoreSets] #list of lists [["asset"], None, ["asset2"]]
	print "restoreAsses:", restoreAsses

	for x in range(3):
		assType = restoreAsses[x]
		if assType:
			for ass in assType:
				assPath = assFolders[x]
				archPath = archFolders[x]

				fullArchPath = "{0}/{1}".format(archPath, ass)
				fullAssPath = "{0}/{1}".format(assPath, ass)
				cFuncs.moveFolder(fullArchPath, fullAssPath)

				print "I've just restored asset: {0}\nFrom: {1}\nTo: {2}".format(ass, fullArchPath, fullAssPath)
	
	#update the assetWin
	if cmds.window("assetWin", exists = True):
		import chrlx_pipe.assetWin as assetWin
		assetWin.populateWindow()

	populateWindow()

def unarchiveAssets(assetFolder, *args):
	#break out the various asset type folders
	charArchs = "{0}/characters/archive".format(assetFolder)
	propArchs = "{0}/props/archive".format(assetFolder)
	setArchs = "{0}/sets/archive".format(assetFolder)

	charAss = "{0}/characters".format(assetFolder)
	propAss = "{0}/props".format(assetFolder)
	setAss = "{0}/sets".format(assetFolder)

	archFolders.append(charArchs)
	archFolders.append(propArchs)
	archFolders.append(setArchs)
	
	assFolders.append(charAss)
	assFolders.append(propAss)
	assFolders.append(setAss)

	unarchiveUI()
