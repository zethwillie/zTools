import maya.cmds as cmds
import chrlxFuncs as funcs
import maya.mel as mel
import os

widgets = {}
env = mel.eval("getenv CHRLX_ROOT")
jobsFolder = os.path.join(env, "jobs")
print "jobs folder (abspath) = %s"%jobsFolder
exclude = [".DS_Store", ".TemporaryItems", ".directory", "Bluearc", "RESTORE", "Thumbs.db"]

def projectWinUI(*args):
	if cmds.window("pWin", exists = True):
		cmds.deleteUI("pWin")

	widgets["mainWin"] = cmds.window("pWin", w=400, h=300, t="Set Project Window", s=True)
	#row layout for two scroll lists
	widgets["mainFLO"] = cmds.formLayout()
	widgets["jobTSL"] = cmds.textScrollList(w=250, h=200, sc=getSpots)
	widgets["spotTSL"] = cmds.textScrollList(w=250, h=200)
	widgets["setBut"] = cmds.button(l="Set Project", w=300, h=30, en=False, bgc = (.3, .3,.3), c=setProject)

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
	cmds.windowPref(widgets["mainWin"], w=400, h=300)
	cmds.showWindow(widgets["mainWin"])

	populateJobs()

def populateJobs(*args):
	#get location of jobs folder
	dirs = os.listdir(jobsFolder)
	dirs.sort()
	for dir in dirs:
		if (dir not in exclude):
			cmds.textScrollList(widgets["jobTSL"], e=True, a=dir)

def getSpots(*args):
	#clear spots list
	cmds.textScrollList(widgets["spotTSL"], e=True, ra=True)
	cmds.button(widgets["setBut"], e=True, en=False, bgc = (.3, .3, .3))
	#get spots for selected job
	sel = cmds.textScrollList(widgets["jobTSL"], q=True, si=True)[0]
	newDir = os.path.join(jobsFolder, sel)
	spots = os.listdir(newDir)
	for spot in spots:
		if spot != "calendar":
			cmds.textScrollList(widgets["spotTSL"], e=True, a=spot, sc = enableButton)

def enableButton(*args):
	cmds.button(widgets["setBut"], e=True, en=True, bgc = (.9, .6, .4))

def setProject(*args):
	#do "funcs.setProject(dirName)"
	job = cmds.textScrollList(widgets["jobTSL"], q=True, si=True)[0]
	spot = cmds.textScrollList(widgets["spotTSL"], q=True, si=True)[0]
	if job and spot:
		path = os.path.join(jobsFolder, job, spot)
		path = path
		cleanPath = funcs.fixpath(path)
		print "passing to setProject func: %s"%cleanPath
		funcs.setProject(cleanPath)
	else:
		cmds.warning("You need to select a job and a spot first!")
def projectSet(*args):
	projectWinUI()