import maya.cmds as cmds
from functools import partial
import os
import json

widgets = {}
dashDB = {}

prefDir = cmds.internalVar(upd = True)

with open(os.path.join(prefDir, "dashboardDB.json"), "r") as f:
	dashDB = json.load(f)
print dashDB

def dashboardUI(*args):
	if cmds.window("dash", exists = True):
		cmds.deleteUI("dash")

	widgets["win"] = cmds.window("dash", t="charlex Dashboard", w=150, h=200)
	widgets["mainCLO"] = cmds.columnLayout()

	widgets["projBut"] = cmds.button(l="projectSetter", w=150, c=partial(execute, "projectSetter"))
	widgets["chrlxBut"] = cmds.button(l="chrlxFuncs", w=150, c=partial(execute, "chrlxFuncs"))

	cmds.showWindow(widgets["win"])

def execute(command, *args):
	print "trying to pass get from DB: %s"%command
	todo = dashDB[command]
	exec(str(todo))

def dashboard(*args):
	dashboardUI()