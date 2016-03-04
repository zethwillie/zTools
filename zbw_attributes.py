########################
#file: zbw_attributes.py
#Author: zeth willie
#Contact: zeth@catbuks.com, www.williework.blogspot.com
#Date Modified: 04/27/13
#To Use: type in python window  "import zbw_attributes as att; att.attributes()"
#Notes/Descriptions: Some basic functions for manipulating channels, attrs and connections
########################

import maya.cmds as cmds
from functools import partial
import maya.mel as mel

#TO-DO----------------add "breakConnections"? disconnect and if they're anim curves delete them.

widgets = {}
colors = {}
colors["red"]=13
colors["blue"]=6
colors["green"]=14
colors["darkRed"]=4
colors["lightRed"]=31
colors["darkBlue"]=5
colors["medBlue"]=15
colors["lightBlue"]=18
colors["royalBlue"]=29
colors["darkGreen"]=7
colors["medGreen"]=27
colors["lightGreen"]=19
colors["yellowGreen"]=26
colors["yellow"]=17
colors["darkYellow"]=21
colors["lightYellow"]=22
colors["purple"]=30
colors["lightPurple"]=9
colors["darkPurple"]=8
colors["black"]=1
colors["white"]=16
colors["brown"]=10
colors["darkBrown"]=11
colors["lightBrown"]=24
colors["pink"]=20
colors["orange"] =12

def attrUI(*args):
	"""UI for the script"""

	if cmds.window("attrWin", exists=True):
		cmds.deleteUI("attrWin")

	widgets["win"] = cmds.window("attrWin", t="zbw_attributes", h=370, w=250, s=True)
	widgets["tabLO"] = cmds.tabLayout()
	widgets["channelColLO"] = cmds.columnLayout("Object/Attr Controls", w=250, bgc=(.8,.8,.8))

	widgets["lockFrLO"] = cmds.frameLayout(l="Lock/Hide", cll=True, w=250, bgc=(.7,.6,.6))
	widgets["lockColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))
	#lock and hide controls

	#switch to Row column layout to break up the channels
	widgets["attrRCLO"] = cmds.rowColumnLayout(nc=2, cw=([1, 100], [2,150]))
	widgets["transCB"] = cmds.checkBox(l="Translates", v=0, cc=partial(enableChannel, "transCB", "translateCBG"))
	widgets["translateCBG"] = cmds.checkBoxGrp(w=150, cw3=(50,50,50), ncb=3, l1="TX", l2="TY", l3="TZ", l4="Vis", va3=(0,0,0), bgc=(.5,.5,.5), en=False)
	widgets["rotCB"] = cmds.checkBox(l="Rotates", v=0, cc=partial(enableChannel, "rotCB","rotateCBG"))
	widgets["rotateCBG"] = cmds.checkBoxGrp(w=150, cw3=(50,50,50), ncb=3, l1="RX", l2="RY", l3="RZ", l4="Vis", va3=(0,0,0), bgc=(.5,.5,.5), en=False)
	widgets["scaleCB"] = cmds.checkBox(l="Scales", v=1, cc=partial(enableChannel, "scaleCB","scaleCBG"))
	widgets["scaleCBG"] = cmds.checkBoxGrp(w=150, cw3=(50,50,50), ncb=3, l1="SX", l2="SY", l3="SZ", l4="Vis", va3=(1,1,1), bgc=(.5,.5,.5), en=True)
	widgets["visCB"] = cmds.checkBox(l="Visibility", v=1)

	#back to frame layout
	cmds.setParent(widgets["lockFrLO"])
	widgets["topOneCLO"] = cmds.columnLayout()
	cmds.separator(h=5, st="none")	
	widgets["lockRBG"] = cmds.radioButtonGrp(nrb=2, l1="Unlock", l2="Lock", sl=2)
	widgets["hideRBG"] = cmds.radioButtonGrp(nrb=2, l1="Show", l2="Hide", sl=2)
	widgets["channelsBut"] = cmds.button(l="Lock/Hide Channels", w=250, h=30, bgc=(.5,.5,.5), rs=True, c=channelLockHide)
	cmds.separator(h=5, st="none")
	widgets["lockAttrTFBG"] = cmds.textFieldButtonGrp(l="Locked Attr", bl="Create", cal=[(1,"left"),(2,"left"),(3,"left")], cw3=[60,135,50], bc=lockedAttr)
	cmds.separator(h=5,st="none")
	widgets["channelsBut"] = cmds.button(l="Move Selected Attr Up", w=250, h=20, bgc=(.5,.7,.5), rs=True, c= partial(shiftAttr, 1))
	widgets["channelsBut"] = cmds.button(l="Move Selected Attr Down", w=250, h=20, bgc=(.7,.5,.5), rs=True, c=partial(shiftAttr, 0))
	cmds.separator(h=5,st="none")

	#back to columnLayout
	cmds.setParent(widgets["channelColLO"])
	widgets["colorFrLO"] = cmds.frameLayout(l="Object Color", cll=True, w=250, bgc=(.7,.6,.6))
	widgets["colorRCLO"] = cmds.rowColumnLayout(nr=4, bgc=(.8,.8,.8))

	#color controls (red, green, blue, yellow, other)
	cmds.canvas(w=50, h=20, rgb=(1,0,0), pc=partial(changeColor, colors["red"]))
	cmds.canvas(w=50, h=20, rgb=(.5,.1,.1), pc=partial(changeColor, colors["darkRed"]))
	cmds.canvas(w=50, h=20, rgb=(.659,.275,.449), pc=partial(changeColor, colors["lightRed"]))
	cmds.canvas(w=50, h=20, rgb=(1,.8,.965), pc=partial(changeColor, colors["pink"]))

	cmds.canvas(w=50, h=20, rgb=(0,1,0), pc=partial(changeColor, colors["green"]))
	cmds.canvas(w=50, h=20, rgb=(0,.35,0), pc=partial(changeColor, colors["darkGreen"]))
	cmds.canvas(w=50, h=20, rgb=(0,.55,.335), pc=partial(changeColor, colors["medGreen"]))
	cmds.canvas(w=50, h=20, rgb=(.35,.635,.15), pc=partial(changeColor, colors["yellowGreen"]))

	cmds.canvas(w=50, h=20, rgb=(0,0,1), pc=partial(changeColor, colors["blue"]))
	cmds.canvas(w=50, h=20, rgb=(0,0,.35), pc=partial(changeColor, colors["darkBlue"]))
	cmds.canvas(w=50, h=20, rgb=(0,.2,.6), pc=partial(changeColor, colors["medBlue"]))
	cmds.canvas(w=50, h=20, rgb=(.65,.8,1), pc=partial(changeColor, colors["lightBlue"]))

	cmds.canvas(w=50, h=20, rgb=(1,1,0), pc=partial(changeColor, colors["yellow"]))
	cmds.canvas(w=50, h=20, rgb=(.225,.1,0), pc=partial(changeColor, colors["darkBrown"]))
	cmds.canvas(w=50, h=20, rgb=(.5,.275,0), pc=partial(changeColor, colors["brown"]))
	cmds.canvas(w=50, h=20, rgb=(.922,.707,.526), pc=partial(changeColor, colors["darkYellow"]))

	cmds.canvas(w=50, h=20, rgb=(.33,0,.33), pc=partial(changeColor, colors["purple"]))
	cmds.canvas(w=50, h=20, rgb=(.2,0,.25), pc=partial(changeColor, colors["darkPurple"]))
	cmds.canvas(w=50, h=20, rgb=(.0,0,.0), pc=partial(changeColor, colors["black"]))
	cmds.canvas(w=50, h=20, rgb=(1,1,1), pc=partial(changeColor, colors["white"]))

#TO-DO----------------figure out breaking connections(to delete or not?), call add attr win
	# cmds.setParent(widgets["channelColLO"])
	# widgets["channelFrLO"] = cmds.frameLayout(l="Channels", cll=True, w=250, bgc=(1,1,1))
	# widgets["channelRCLO"] = cmds.columnLayout(bgc=(.8,.8,.8))
	# widgets["breakAllBut"] = cmds.button(l="Break All Connections", w=150, h=30, bgc=(.5,.5,.5))
	# widgets["breakSelBut"] = cmds.button(l="Break Selected Connections", w=150, h=30, bgc=(.5,.5,.5))
	# cmds.separator(h=10, st="none")
	# widgets["addAttBut"] = cmds.button(l="Show 'Add Attribute' win", w=150, h=30, bgc=(.5,.5,.5))

	cmds.setParent(widgets["tabLO"])
	widgets["connectColLO"] = cmds.columnLayout("Connections", w=250, bgc=(.8,.8,.8))
	widgets["connectFrame"] = cmds.frameLayout(l="Make General Connections", cll=True, bgc=(.6,.8,.6))
	widgets["connectionColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))

	#connection stuff
	cmds.text("Select a source object and a channel:")
	widgets["connector"] = cmds.textFieldButtonGrp(l="Connector", w=250, bl="<<<", cal=[(1,"left"),(2,"left"),(3,"left")], cw3=[60,140,30], bc=partial(getChannel, "connector"))
	cmds.separator(h=5,st="none")
	cmds.text("Select a target object and channel:")
	widgets["connectee"] = cmds.textFieldButtonGrp(l="Connectee", w=250, bl="<<<", cal=[(1,"left"),(2,"left"),(3,"left")], cw3=[60,140,30], bc=partial(getChannel, "connectee"))
	cmds.separator(h=10,st="none")
	widgets["connectBut"] = cmds.button(l="Connect Two Channels", w=240, h=30, bgc=(.5,.5,.5), c=connectChannels)
	cmds.separator(h=5,st="none")

	cmds.setParent(widgets["connectColLO"])
	widgets["shapeFrame"] = cmds.frameLayout(l="Connect to Shape Visibility", cll=True, bgc=(.6,.8,.6))
	widgets["shapeColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))

	widgets["toShapeVis"] = cmds.textFieldButtonGrp(l="Vis Driver", w=250, bl="<<<", cal=[(1,"left"),(2,"left"),(3,"left")], cw3=[60,140,30], bc=partial(getChannel, "toShapeVis"))
	cmds.separator(h=5,st="none")
	cmds.text("Now select the objs to drive:")
	widgets["shapeBut"] = cmds.button(l="Connect to Shapes' vis", w=240, h=30, bgc=(.5,.5,.5), c=connectShapeVis)
	cmds.separator(h=5,st="none")

	cmds.setParent(widgets["connectColLO"])
	widgets["inoutFrame"] = cmds.frameLayout(l="Select Connections (and print)", cll=True, bgc=(.6,.8,.6))
	widgets["inOutColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))

	widgets["conversionCB"] = cmds.checkBox(l="Skip 'conversion' nodes?", v=1)
	cmds.text("Select an attribute in the channel box:")
	widgets["getInputBut"] = cmds.button(l="Select inConnection object", w=240, h=30, bgc=(.5,.5,.5), c=getInput)
	widgets["getOutputBut"] = cmds.button(l="Select outConnection objects", w=240, h=30, bgc=(.5,.5,.5), c=getOutput)

	#show window
	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=250, h=370)


def enableChannel(source, target, *args):
	"""This function enables or disables the indiv channel checkboxes when attr is toggled"""

	CBG = widgets[target]
	on = cmds.checkBox(widgets[source], q=True, v=True)
	if on:
		cmds.checkBoxGrp(CBG, e=True, en=True, va3=(1,1,1))
	else:
		cmds.checkBoxGrp(CBG, e=True, en=False, va3=(0,0,0))

def channelLockHide(*args):
	"""this is the function to actually do the locking and hiding of the attrs selected in the UI"""

	sel = cmds.ls(sl=True, type="transform")
	if sel:
		channels = []
		tx = cmds.checkBoxGrp(widgets["translateCBG"], q=True, v1=True)
		ty = cmds.checkBoxGrp(widgets["translateCBG"], q=True, v2=True)
		tz = cmds.checkBoxGrp(widgets["translateCBG"], q=True, v3=True)

		rx = cmds.checkBoxGrp(widgets["rotateCBG"], q=True, v1=True)
		ry = cmds.checkBoxGrp(widgets["rotateCBG"], q=True, v2=True)
		rz = cmds.checkBoxGrp(widgets["rotateCBG"], q=True, v3=True)

		sx = cmds.checkBoxGrp(widgets["scaleCBG"], q=True, v1=True)
		sy = cmds.checkBoxGrp(widgets["scaleCBG"], q=True, v2=True)
		sz = cmds.checkBoxGrp(widgets["scaleCBG"], q=True, v3=True)

		v = cmds.checkBox(widgets["visCB"], q=True, v=True)

		lock = cmds.radioButtonGrp(widgets["lockRBG"], q=True, sl=True)
		key = cmds.radioButtonGrp(widgets["hideRBG"], q=True, sl=True)

		if lock == 1:
			lock = 0
		elif lock == 2:
			lock = 1
		if key == 1:
			key = 1
		elif key == 2:
			key = 0

		attrs = {"tx":tx, "ty":ty, "tz":tz, "rx":rx, "ry":ry, "rz":rz, "sx":sx, "sy":sy, "sz":sz, "v":v}
		for attr in attrs:
			if attrs[attr]:
				channels.append("%s"%attr)

		for obj in sel:
			for channel in channels:
				cmds.setAttr("%s.%s"%(obj, channel), l=lock)
				cmds.setAttr("%s.%s"%(obj, channel), k=key)
	else:
		cmds.warning("You haven't selected anything!")

def lockedAttr(*args):
	"""creates a locked attr (I use as a separator). Uses the long name as the nice name (literal name in channel box)"""
	attrName = cmds.textFieldButtonGrp(widgets["lockAttrTFBG"], q=True, tx=True)
	print attrName
	
	if attrName:
		sel = cmds.ls(sl=True)

		if sel:
			for obj in sel:
				try:
					cmds.addAttr(obj, ln=attrName, nn=attrName, at="enum", en="-----", k=True)
					cmds.setAttr("%s.%s"%(obj, attrName), l=True)
				except:
					cmds.warning("Failed to add %s to %s, skipping!"%(attrName, obj))
		else:
			cmds.warning("Please select some objects to add attr to!")
	else:
		cmds.warning("Please enter a name for the attr!")

def shiftAttr(mode, *args):
	"""shifts the selected attr up or down"""

	obj = cmds.channelBox('mainChannelBox',q=True,mol=True)
	if obj:
		attr = cmds.channelBox('mainChannelBox',q=True,sma=True)
		if attr:
			for eachObj in obj:
				udAttr = cmds.listAttr(eachObj,ud=True)
				if not attr[0] in udAttr:
					sys.exit('selected attribute is static and cannot be shifted')
				#temp unlock all user defined attributes
				attrLock = cmds.listAttr(eachObj,ud=True,l=True)
				if attrLock:
					for alck in attrLock:
						cmds.setAttr(eachObj + '.' + alck,lock=0)
				#shift down
				if mode == 0:
					if len(attr) > 1:
						attr.reverse()
						sort = attr
					if len(attr) == 1:
						sort = attr 
					for i in sort:
						attrLs = cmds.listAttr(eachObj,ud=True)
						attrSize = len(attrLs)
						attrPos = attrLs.index(i)
						cmds.deleteAttr(eachObj,at=attrLs[attrPos])
						cmds.undo()
						for x in range(attrPos+2,attrSize,1):
							cmds.deleteAttr(eachObj,at=attrLs[x])
							cmds.undo()
				#shift up 
				if mode == 1:
					for i in attr:
						attrLs = cmds.listAttr(eachObj,ud=True)
						attrSize = len(attrLs)
						attrPos = attrLs.index(i)
						if attrLs[attrPos-1]:
							cmds.deleteAttr(eachObj,at=attrLs[attrPos-1])
							cmds.undo()
						for x in range(attrPos+1,attrSize,1):
							cmds.deleteAttr(eachObj,at=attrLs[x])
							cmds.undo()
				#relock all user defined attributes			
				if attrLock:
					for alck in attrLock:
						cmds.setAttr(eachObj + '.' + alck,lock=1)

def changeColor(color, *args):
	"""changes the shape node color of the selected objects"""

	sel = cmds.ls(sl=True, type="transform")
	if sel:
		for obj in sel:
			shapes = cmds.listRelatives(obj, s=True)
			for shape in shapes:
				cmds.setAttr("%s.overrideEnabled"%shape, 1)
				cmds.setAttr("%s.overrideColor"%shape, color)

def breakConnections(*args):
	#disconnectAttr
	pass

def getChannel(tfbg, *args):
	"""gets the selected channel of the selected objects"""

	obj = ""
	channel = ""

	cBox = mel.eval('$temp=$gChannelBoxName')
	sel = cmds.ls(sl=True, l=True)

	if sel:
		if not len(sel)==1:
			cmds.warning("You have to select ONE node!")
		else:
			obj = sel[0]
	else:
		cmds.warning("You have to select ONE node!")

	if sel:
		channels = cmds.channelBox(cBox, q=True, sma=True, ssa=True, sha=True, soa=True)

		if channels:
			if not len(channels) == 1:
				cmds.warning("You have to select ONE channel!")
			else:
				channel = channels[0]
		else:
			cmds.warning("You have to select ONE channel!")

	if obj and channel:
		full = "%s.%s"%(obj, channel)
		cmds.textFieldButtonGrp(widgets[tfbg], e=True, tx=full)

def connectChannels(*args):
	"""connects two channels together from the test fields"""

	connector = cmds.textFieldButtonGrp(widgets["connector"], q=True, tx=True)
	connectee = cmds.textFieldButtonGrp(widgets["connectee"], q=True, tx=True)
	try:
		cmds.connectAttr(connector, connectee, f=True)
		print "Connected %s -----> %s"%(connector, connectee)
	except:
		cmds.warning("Couldn't connect those attrs. . . Sorry!")

def getInput(*args):
	""" collects the input from the selected obj.channel"""

	obj = ""
	channel = ""
	conv = cmds.checkBox(widgets["conversionCB"], q=True, v=True)

	cBox = mel.eval('$temp=$gChannelBoxName')
	sel = cmds.ls(sl=True, l=True)

	if sel:
		if not len(sel)==1:
			cmds.warning("You have to select ONE node!")
		else:
			obj = sel[0]
	else:
		cmds.warning("You have to select ONE node!")

	if sel:
		channels = cmds.channelBox(cBox, q=True, sma=True, ssa=True, sha=True, soa=True)

		if channels:
			if not len(channels) == 1:
				cmds.warning("You have to select ONE channel!")
			else:
				channel = channels[0]
		else:
			cmds.warning("You have to select ONE channel!")

	if obj and channel:
		full = "%s.%s"%(obj, channel)
		inAttr = cmds.listConnections(full, plugs=True, scn=conv, d=False, s=True)
		if inAttr:
			for each in inAttr:
				print "%s -----> %s"%(each, full)
		else:
			cmds.warning("No input connections on this attr!")
		inNodes = cmds.listConnections(full, scn=conv, d=False, s=True)
		if inNodes:
			cmds.select(cl=True)
			for node in inNodes:
				cmds.select(node, add=True)

def getOutput(*args):
	""" collects the outputs from the selected obj.channel"""

	obj = ""
	channel = ""
	conv = cmds.checkBox(widgets["conversionCB"], q=True, v=True)

	cBox = mel.eval('$temp=$gChannelBoxName')
	sel = cmds.ls(sl=True, l=True)

	if sel:
		if not len(sel)==1:
			cmds.warning("You have to select ONE node!")
		else:
			obj = sel[0]
	else:
		cmds.warning("You have to select ONE node!")

	if sel:
		channels = cmds.channelBox(cBox, q=True, sma=True, ssa=True, sha=True, soa=True)

		if channels:
			if not len(channels) == 1:
				cmds.warning("You have to select ONE channel!")
			else:
				channel = channels[0]
		else:
			cmds.warning("You have to select ONE channel!")

	if obj and channel:
		full = "%s.%s"%(obj, channel)
		outAttr = cmds.listConnections(full, plugs=True, scn=conv, d=True, s=False)
		if outAttr:
			for each in outAttr:
				print "%s ----> %s"%(full,each)
		else:
			cmds.warning("No output connections on this attr!")
		outNodes = cmds.listConnections(full, scn=conv, d=True, s=False)
		if outNodes:
			cmds.select(cl=True)
			for node in outNodes:
				cmds.select(node, add=True)

def connectShapeVis(*args):
	"""Connects the attr from the assoc. text field to the shape Visibility of selected objects"""

	sel = cmds.ls(sl=True, type="transform")
	driver = cmds.textFieldButtonGrp(widgets["toShapeVis"], q=True, tx=True)

	if sel:
		if driver:
			for obj in sel:
				shapes = cmds.listRelatives(obj, s=True)
				for shape in shapes:
					try:
						cmds.connectAttr(driver, "%s.v"%shape, f=True)
						cmds.warning("Connected %s to %s"%(driver, shape))
					except:
						cmds.warning("Couldn't connect %s to %s. Sorry! Check the Script Editor."%(driver, shape))
	else:
		cmds.warning("You need to select an object to connect the shape.vis!")

def attributes(*args):
	"""Use this to start the script!"""

	attrUI()