import maya.cmds as cmds
import maya.mel as mel
import os
from functools import partial
import chrlx_pipe.chrlxFuncs as cFuncs

widgets = {}

def exportUI(*args):
	
	if cmds.window("expUIWin", exists = True):
		cmds.deleteUI("expUIWin")
		
	widgets["win"] = cmds.window("expUIWin", w=300, h=250, t="Export FBX")
	widgets["tabLO"] = cmds.tabLayout(w=300, h=250)
	widgets["rigCLO"] = cmds.columnLayout("Rig Export", w=300, h=250)
	
	cmds.text(l= "Select the group with the root joint and geo group")
	cmds.separator(h=10)
	widgets["pathTFBG"] = cmds.textFieldButtonGrp(l="Folder:", bl=">>", cal = [(1, "left"), (2, "left"), (3, "left")], cw=[(1, 50), (2, 200), (3, 50)], bc = partial(getLoc, "pathTFBG"))
	widgets["nameTFG"]	= cmds.textFieldGrp(l="Name:",cal = [(1, "left"), (2, "left")], cw=[(1, 50), (2, 200)])
	cmds.separator(h=10)	
	widgets["rigExpBut"] = cmds.button(l="Export Rig FBX", w=300, h=30, bgc =(.5,.8, .5), c=partial(fileAction, "fbxexp"))
	
	cmds.setParent(widgets["tabLO"])
	widgets["animCLO"] = cmds.columnLayout("Anim Export", w=300, h=250)
	widgets["mayaTFBG"] = cmds.textFieldButtonGrp(l="Folder:", bl=">>", cal = [(1, "left"), (2, "left"), (3, "left")], cw=[(1, 50), (2, 200), (3, 50)], bc = partial(getLoc, "mayaTFBG"))
	widgets["animNameTFG"]	= cmds.textFieldGrp(l="AnimName:",cal = [(1, "left"), (2, "left")], cw=[(1, 50), (2, 200)])
	cmds.separator(h=10)
	cmds.text(l="1. Select the export hierarchy with the joints")
	widgets["expMaBut"] = cmds.button(l="2. export selected as .ma file", w=300, bgc = (.7, .7,.7), c=partial(fileAction, "mayaexp"))
	widgets["openMaBut"] = cmds.button(l="3. open maya file", w=300, bgc = (.7, .7,.7), c=partial(fileAction, "openMaya"))
	widgets["jointBut"] = cmds.button(l="4. select all joints", w=300, bgc = (.7, .7,.7), c=selectJoints)
	widgets["bakeBut"] = cmds.button(l="5. bake all joints (based on timeline)", w=300, bgc = (.7, .7,.7), c=bakeJoints)
	widgets["crnBut"] = cmds.button(l="6. open comet rename (to clean names)", w=300, bgc = (.7, .7,.7), c=cometRN)
	widgets["expAnmBut"] = cmds.button(l="7. (after cleaning names and dag) export final fbx", w=300, bgc = (.7, .7,.7), c=partial(fileAction, "animFbx"))

	cmds.showWindow(widgets["win"])

def fileAction(action="", *args):
	"""
	exports the info in the window as fbx
	"""
	if action == "fbxexp":
		pathFld = "pathTFBG"
		nameFld = "nameTFG"
		suffix = "fbx"
	elif action == "mayaexp" or "openMaya":
		pathFld = "mayaTFBG"
		nameFld = "animNameTFG"
		suffix = "ma"
	elif action == "animFbx":
		pathFld = "mayaTFBG"
		nameFld = "animNameTFG"
		suffix = "fbx"
				
	folder = cmds.textFieldButtonGrp(widgets[pathFld], q=True, tx=True)
	expName = cmds.textFieldGrp(widgets[nameFld], q=True, tx=True)
	fileName = "{0}.{1}".format(expName, suffix)
	
	if folder and expName:
		path = cFuncs.fixPath(os.path.join(folder, fileName))
		if action == "fbxexp":
			expFbx(path)
		elif action == "mayaexp":
			cmds.file(path, force=True, type="mayaAscii", exportSelected= True)
		elif action == "animFbx":
			expFbx(path)
		elif action == "openMaya":
			cmds.file(path, open=True, force=True)
	else:
		cmds.warning("You need to have a location AND a file name")

def bakeJoints(*args):
	jnts = cmds.ls(sl=True)
	
	range = getSliderRange()
	cmds.bakeResults(jnts, time=range, sampleBy=1, simulation = True)
	
def cometRN(*args):
	mel.eval("cometRename")

def getSliderRange(*args):
    """gets framerange in current scene and returns start and end frames"""

    #get timeslider range start
    startF = cmds.playbackOptions(query=True, min=True)
    endF = cmds.playbackOptions(query=True, max=True)
    return(startF, endF)

def selectJoints(*args):
	sel = cmds.ls(type="joint")
	cmds.select(sel, r=True)

def getLoc(field, *args):
	"""
	get location, put it in the tfbg
	"""
	path = cFuncs.fixPath(cmds.fileDialog2(fileMode = 2, ds=1)[0])
	cmds.textFieldButtonGrp(widgets[field], e=True, tx = path)

def expFbx(path, *args):
	cmds.file(path, force=True, type="Fbx", exportSelected= True)
	
exportUI()


#root = cmds.ls(sl=True)[0]

#children = cmds.listRelatives(root, ad=True)

#for obj in children:
	#if (cmds.objectType(obj) == "parentConstraint") or (cmds.objectType(obj) == "scaleConstraint") or (cmds.objectType(obj) == "orientConstraint") or (cmds.objectType(obj) == "pointConstraint"):
#	if (cmds.objectType(obj) == "joint"):
#		cmds.bakeSimulation(obj)

