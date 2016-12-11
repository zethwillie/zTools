import maya.cmds as cmds
from functools import partial
import os
import json

widgets = {}
dashDB = {}

prefDir = cmds.internalVar(upd = True)

####check that this files exists, raise if not

with open(os.path.join(prefDir, "dashboardDB.json"), "r") as f:
	dashDB = json.load(f)

def dashboardUI(*args):
	if cmds.window("dash", exists = True):
		cmds.deleteUI("dash")

	widgets["win"] = cmds.window("dash", t="charlex Dashboard", w=150, h=200)
	widgets["mainCLO"] = cmds.columnLayout()

	widgets["projBut"] = cmds.button(l="projectSetter", w=150, c=partial(execute, "projectSetter"))
	#widgets["chrlxBut"] = cmds.button(l="chrlxFuncs", w=150, c=partial(execute, "chrlxFuncs"))
	widgets["fileWinBut"] = cmds.button(l="chrlxFileWin", w=150, c=partial(execute, "fileWin"))
	widgets["camExportBut"] = cmds.button(l="camExporter", w=150, c=partial(execute, "camExporter"))
	widgets["pvShaderBut"] = cmds.button(l="previsShaders", w=150, c=partial(execute, "previsShaders"))	
	widgets["assetWinBut"] = cmds.button(l="assetWin", w=150, bgc = (.8, .6, .5), c=partial(execute, "assetWin"))
	widgets["shotWinBut"] = cmds.button(l="shotWin", w=150, bgc = (.7, .8, .5), c=partial(execute, "shotWin"))

	cmds.showWindow(widgets["win"])

def execute(command, *args):
	todo = dashDB[command]
	print "dashboard is about to try: {0}".format(todo)
	exec(str(todo))

def dashboard(*args):
	dashboardUI()

#######-- if dashboardDB.json file doesn't exist, then grab it from the scripts dir (where this script lives and drop it in user prefs)
#######-- create a way to quickly register a script and add to the dashboard? 