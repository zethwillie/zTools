import maya.cmds as cmds
import chrlx_pipe.chrlxFuncs as funcs
reload(funcs)
import maya.mel as mel
import os
from functools import partial

######## get proper env var for root of jobs folder(line 9)


widgets = {}
passWin = None
UIField = None
#env = mel.eval("getenv CHRLX_ROOT")
#jobsFolder = os.path.join(env, "jobs")
jobsFolder = "//Bluearc/GFX/jobs"

exclude = [".DS_Store", ".TemporaryItems", ".directory", "Bluearc", "RESTORE", "Thumbs.db"]

def projectWinUI(passWin=None, UIField=None, assType = None, *args):
	if cmds.window("psWin", exists = True):
		cmds.deleteUI("psWin")

	widgets["mainWin"] = cmds.window("psWin", w=400, h=300, t="Set Project Window", s=True)
	#row layout for two scroll lists
	widgets["mainFLO"] = cmds.formLayout()
	widgets["jobTSL"] = cmds.textScrollList(w=250, h=200, sc=getSpots)
	widgets["spotTSL"] = cmds.textScrollList(w=250, h=200)
	widgets["setBut"] = cmds.button(l="Set Project", w=300, h=30, en=False, bgc = (.3, .3,.3), c=partial(setProject, passWin, UIField, assType))

	cmds.formLayout(widgets["mainFLO"], e=True, af = [
		(widgets["jobTSL"], "top", 0), 
		(widgets["jobTSL"], "left", 0), 
		(widgets["jobTSL"], "bottom", 50)])
	cmds.formLayout(widgets["mainFLO"], e=True, af = [
		(widgets["spotTSL"], "top", 0),
		(widgets["spotTSL"], "right", 0), 
		(widgets["spotTSL"], "bottom", 50)])
	cmds.formLayout(widgets["mainFLO"], e=True, af = [
		(widgets["setBut"], "bottom", 0), 
		(widgets["setBut"], "left", 0), 
		(widgets["setBut"], "bottom", 0), 
		(widgets["setBut"], "right", 0)])

	cmds.formLayout(widgets["mainFLO"], e=True, ac = [
		(widgets["jobTSL"], "right", 10, widgets["spotTSL"])
		])
	cmds.window(widgets["mainWin"], e=True, w=400, h=300)
	cmds.showWindow(widgets["mainWin"])

	populateJobs()

def populateJobs(*args):
	#get location of jobs folder
	dirs = os.listdir(jobsFolder)
	dirlist = []
	for dir in dirs:
		if (dir not in exclude) and (dir[0] != ".") and (dir[0] != "_"):
			dirlist.append(dir)	
	dirlist.sort()
	for dir in dirlist:
		cmds.textScrollList(widgets["jobTSL"], e=True, a=dir)

def getSpots(*args):
	#clear spots list
	cmds.textScrollList(widgets["spotTSL"], e=True, ra=True)
	cmds.button(widgets["setBut"], e=True, en=False, bgc = (.3, .3, .3))
	#get spots for selected job
	sel = cmds.textScrollList(widgets["jobTSL"], q=True, si=True)[0]
	newDir = os.path.join(jobsFolder, sel)
	spots = os.listdir(newDir)
	spotlist = []
	for spot in spots:
		#create list of null folders and below say if not in list:
		if spot != "calendar" and (spot[0] != ".") and (spot[0] != "_"):
			spotlist.append(spot)
	spotlist.sort()
	for spot in spotlist:
			cmds.textScrollList(widgets["spotTSL"], e=True, a=spot, sc = enableButton)

def enableButton(*args):
	cmds.button(widgets["setBut"], e=True, en=True, bgc = (.9, .6, .4))

def setProject(passWin=None, UIField=None, assType = None, *args):
	#set project to proper folder!!! project is 3D folder!!!
	job = cmds.textScrollList(widgets["jobTSL"], q=True, si=True)[0]
	spot = cmds.textScrollList(widgets["spotTSL"], q=True, si=True)[0]

	if job and spot:

		path = os.path.join(jobsFolder, job, spot, "3d")
		cleanPath = funcs.fixPath(path)

		#sets project via chrlxFuncs
		if os.path.isdir(cleanPath) and (passWin != "dupe"):
			funcs.setProject(cleanPath)
			cmds.deleteUI("psWin")
		elif os.path.isdir(cleanPath) and (passWin == "dupe"):
			cmds.deleteUI("psWin")
			outProj = cleanPath
		else:
			cmds.error("The selected project is not in the correct schema for these pipeline tools")

		#reset fileWin or do output thingy based on passed in info
		if passWin == "asset":
			if cmds.window("assetWin", exists=True):
				import chrlx_pipe.assetWin as fileWin
				fileWin.populateWindow()
		if passWin == "shot":
			if cmds.window("shotWin", exists=True):
				import chrlx_pipe.shotWin as fileWin
				fileWin.populateWindow()
		if passWin == "dupe":
			if cmds.window("dupeWin", exists=True):
				cmds.textFieldButtonGrp(UIField, e=True, tx=funcs.fixPath(os.path.join(cleanPath, "assets", assType)))

	else:
		cmds.warning("You need to select a job and a spot first!")


def projectSetter(window = None, field = None, assType = None, *args):
	passWin =  window
	projectWinUI(passWin, field, assType)
