###########
# quick increment - just a little window to increment when you're in a workshop file
###########

import os
import maya.cmds as cmds
import chrlx.utils as utils
import chrlx_pipe.chrlxFuncs as cFuncs

widgets = {}

def quickInrementUI(*args):
	"""win for quick increment"""
	if cmds.window("qiwin", exists=True):
		cmds.deleteUI("qiwin")

	widgets["win"] = cmds.window("qiwin", t="Increment WS", w=200, h=75, s=False)

	widgets["mainCLO"] = cmds.columnLayout()
	widgets["incrBut"] = cmds.button(l="Increment Current WS!", bgc = (.9, .5, .5), w=200, h=75, c=increment)

	cmds.window(widgets["win"], e=True, w=200, h=75)
	cmds.showWindow(widgets["win"])


def increment(*args):
	#get current scene
	curr = cFuncs.fixPath(cmds.file(q=True, sn=True))
	#check that we're in schema 2
	if curr:
		pm = utils.PathManager(curr)
		basename = os.path.basename(curr)

		if pm.spotSchema == 2 and (basename[-8:-6]=="_v"): #check that we're in a ws file in correct proj type
	######### -------- if asset. . .		
			asset = basename.partition("_")[0]
			split = curr.partition("/assets/")
			head = cFuncs.fixPath(split[0] + split[1])
			assetFolder = cFuncs.fixPath(os.path.join(head, split[2].partition("/")[0], asset))
			fType = split[2].partition("/{}/".format(asset))[2].partition("/")[0]
			print fType
			incrementFile = cFuncs.incrementWS(asset, assetFolder, fType)
			wsNum = int(os.path.basename(incrementFile).rstrip(".ma").rpartition("_")[2].strip("v"))
			cmds.file(rename = incrementFile + ".ma")
			cFuncs.putFileInfo(fType, wsNum , "quick increment", *args)
			cmds.file(save=True, type="mayaAscii")

			if cmds.window("assetWin", exists=True):
				import chrlx_pipe.assetWin as assWin
				assWin.populateWindow(asset)
		else:
			cmds.warning("You're not in a file I can increment (either wrong project schema or not in a workshop)")
	else:
		cmds.warning("You seem to be in an unsaved scene! No workshop to increment!")

def quickIncrement(*args):
	quickInrementUI()
