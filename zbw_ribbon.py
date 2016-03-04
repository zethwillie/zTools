########################
#file: zbw_ribbon.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com
#date modified: 09/23/12
#
#notes: calls the class that creates the ribbon (instance is "ribbon"). The UI has options for a few things . . . .
#call with: import zbw_ribbon; zbw_ribbon.zbw_ribbon()
########################

import zbw_rig as rig
import zbw_window as win
import maya.OpenMaya as om
import maya.cmds as cmds


#----------------create a bezier version of this (4 divisions, don't need control joints, create cluster setups and attrs to use them, create aim constraints for end joints)


#----------figure out how to make midpoint adjustable (visually???) . . .
class RibbonUI(win.Window):
	def __init__(self):
		self.windowName = "zbw_ribbon"
		self.windowSize = [420, 280]
		self.sizeable = 1

		self.createUI()

	def commonUI(self):
		pass

	def customUI(self):
		self.widgets["ribbonNameTFG"] = cmds.textFieldGrp(l="Ribbon Rig Name", cal=[(1, "left"), (2, "left")], cw=[(1, 100), (2, 200)], tx="ribbon")
		cmds.separator(h=10, style="single")
		self.widgets["jointsIFG"] = cmds.intFieldGrp(l="Number of Jnts (3 min)", cal=([1,"left"]), cw=([1, 125], [2,100]),v1=5)
		self.widgets["axis"] = cmds.radioButtonGrp(l="Ribbon Ctrl Axis", nrb=3, l1="x", l2="y", l3="z", cal=([1,"left"]), cw=([1, 125], [2,50], [3,50]), sl=2, en=True)
		self.widgets["fkSetupCB"] = cmds.checkBox(l="Setup FK Controls", v=1)
		self.widgets["heightFFG"] = cmds.floatFieldGrp(l="Ribbon Height", cal= [(1, "left"), (2, "left")], cw= [(1, 125), (2, 100)], v1=10.0)
		self.widgets["ratioFFG"] = cmds.floatFieldGrp(l="Heigth/width Ratio", cal= [(1, "left"), (2, "left")], cw= [(1, 125), (2, 100)], v1=5)
		#create a slider for where we want the middle piece of the ribbon
		self.widgets["centerPosFSG"] = cmds.floatSliderGrp(l="Center Ctrl Position", f=True, cal = [(1, "left"), (2,"left"), (3,"left")], cw=[(1, 125), (2, 50), (3, 200)], min=0, max=1, fmn=0, fmx=1, v=0.5, pre=3)
		#option for making (or not) control structure
		#-------option to use my own surface?
		self.widgets["existingGeoCB"] = cmds.checkBox(l="Use existing nurbs curve", v=0, cc=self.geoEnable)
		#this will reveal text field grp w button
		#checking and unchecking will activate options (and deactivate)
		self.widgets["geoTFBG"] = cmds.textFieldButtonGrp(l="Select Geometry", bl="<<<", en=False, cal=[(1,"left"), (2, "left"), (3, "left")], cw=[(1, 100), (2, 250), (3, 50)], bc=self.getGeo)
		self.widgets["directionRBG"] = cmds.radioButtonGrp(l="Along U or V?", nrb=2, l1="u", l2="v", cal=[(1, "left"), (2, "left")], cw=[(1, 100), (2,50), (3,50)], sl=2, en=False)

#----------------deal better with the x, y, z (should be "+x", "-x", etc)
		#option for indiv follicle controls?

	def action(self, close, *args):
		#do the action here
		self.createRibbon()

		#close window
		if close:
			self.closeWindow()
		pass

	def printHelp(self, *args):
		#########  modify for inheritence ###########
		print("this is your help, yo")

	def resetValues(self, *args):
		#########  modify for inheritence ###########
		print("test values reset")

	def saveValues(self, *args):
		#########  modify for inheritence ###########
		print("test save values")

	def loadValues(self, *args):
		#########  modify for inheritence ###########
		print("test load values")

	def geoEnable(self, *args):
		#toggle the enable
		#get the state of the button
		state = cmds.checkBox(self.widgets["existingGeoCB"], q=True, v=True)
		if state:
			cmds.textFieldButtonGrp(self.widgets["geoTFBG"], e=True, en=True)
			cmds.radioButtonGrp(self.widgets["directionRBG"], e=True, en=True)
			cmds.floatFieldGrp(self.widgets["heightFFG"], e=True, en=False)
			cmds.floatFieldGrp(self.widgets["ratioFFG"] , e=True, en=False)
			#cmds.textFieldGrp(self.widgets["ribbonNameTFG"], e=True, en=False)
		else:
			cmds.textFieldButtonGrp(self.widgets["geoTFBG"], e=True, en=False)
			cmds.radioButtonGrp(self.widgets["directionRBG"], e=True, en=False)
			cmds.floatFieldGrp(self.widgets["heightFFG"], e=True, en=True)
			cmds.floatFieldGrp(self.widgets["ratioFFG"] , e=True, en=True)
			#cmds.textFieldGrp(self.widgets["ribbonNameTFG"], e=True, en=True)

	def getGeo(self, *args):
		#get selection and put it's full path into the tfbg
		sel = cmds.ls(sl=True, type="transform", l=True)
		print(sel)
		if len(sel) != 1:
			cmds.warning("yo. Select one and only one nurbs surface")
		else:
			#check for nurbsy-ness
			if (cmds.objectType(cmds.listRelatives(sel[0], shapes=True)[0])!="nurbsSurface"):
				cmds.error("Selected is not a nurbs surface")
			else:
				cmds.textFieldButtonGrp(self.widgets["geoTFBG"], e=True, tx=sel[0])


	def createRibbon(self, *args):
		self.name = cmds.textFieldGrp(self.widgets["ribbonNameTFG"], q=True, tx=True)
		self.numDiv = (cmds.intFieldGrp(self.widgets["jointsIFG"], q=True, v=True)[0]) -1
		self.fk = cmds.checkBox(self.widgets["fkSetupCB"], q=True, v=True)
		self.height = cmds.floatFieldGrp(self.widgets["heightFFG"], q=True, v1=True)
		self.ratio = cmds.floatFieldGrp(self.widgets["ratioFFG"], q=True, v1=True)
		self.axis = cmds.radioButtonGrp(self.widgets["axis"] , q=True, sl=True)

		print("axis = :%s"%self.axis)
		self.ribbonName = "%s_ribbonGeo"%self.name
		self.numJoints = self.numDiv
		self.follicleList = []
		self.follicleJntList = []
		self.own = cmds.checkBox(self.widgets["existingGeoCB"], q=True, v=True)
		self.myGeo = cmds.textFieldButtonGrp(self.widgets["geoTFBG"], q=True, tx=True)
		self.dir = cmds.radioButtonGrp(self.widgets["directionRBG"], q=True, sl=True )
		print("dir: %s"%self.dir)
		self.centerPos = cmds.floatSliderGrp(self.widgets["centerPosFSG"], q=True, v=True )
		self.follicleGrpList = []

#-----------make sure the num of divisions is at least 1
#-----------create the nurbs plane in the correct axis (just make the plane in the axis and figure out how to rotate joint local rotational axes to match it) DON'T WORRY ABOUT THIS SO MUCH (IT'S HIDDEN), WORRY ABOUT THE CONTROLS BEING ORIENTED CORRECTLY!!!

		if self.own == 0:
			self.dir = 2
		if self.dir == 1:
			dir = "u"
			uDiv = self.numDiv
			vDiv = 1
		else:
			dir = "v'"
			uDiv = 1
			vDiv = self.numDiv

		# if self.axis  == 1:
		axis = [0, 0, 1]
		# elif self.axis  == 2:
		# 	axis = [0, 1, 0]
		# elif self.axis  == 3:
		# 	axis = [0, 0, 1]

		if self.own == 0:
			width = self.height/self.ratio
			#create the nurbsPlane
			cmds.nurbsPlane(ax=axis, w=width, lr=self.ratio, d=3, u=uDiv, v=vDiv, ch=0, n=self.ribbonName)
			cmds.rebuildSurface (self.ribbonName, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kc=0, su=1, du=1, sv=self.numDiv, dv=3, tol=0.1, fr=0, dir=0)
			cmds.move(0, self.height/2, 0, self.ribbonName)

			cmds.xform(self.ribbonName, ws=True, rp=[0, 0, 0])
		else:
			self.ribbonName = self.myGeo

		#find the ratio for the uv's (one dir will be .5, the other a result of the num joints)
		factor = 1.0/self.numJoints

#-------keep follicle joints separate, not parente under each follicle, separate group for those
#-------follicle jnts each go under a ctrl (star) that is under a group. That group gets parent constrained to the follicles
#-------these joints should be aligned with the follicles??? does that make a difference?

		#create the follicles on the surface, joints on the follicles
		for x in range (self.numJoints+1):
			val = x * factor
			folName = "%s_follicle%s"%(self.name, x)
			#create a follicle in the right direction
			if self.dir ==1:
				follicle = rig.follicle(self.ribbonName, folName, val, 0.5)[0]
			else:
				follicle = rig.follicle(self.ribbonName, folName, 0.5, val)[0]

			self.follicleList.append(follicle)

			#create joint and parent to follicle
			jointName = "%s_fol%s_JNT"%(self.name, x)
#---------have to figure out how to orient this correctly (just translate and rotate the joints (or the controls they're under))
			#create joint control? then move the control and the joint under it to the correct rot and pos
			folPos = cmds.xform(follicle, q=True, ws=True, t=True)
			folRot = cmds.xform(follicle, q=True, ws=True, ro=True)
			cmds.select(cl=True)
			folJoint = cmds.joint(n=jointName, p=(0,0,0))
			folGroup = cmds.group(folJoint, n="%s_GRP"%folJoint) #this could become control for the joint
			cmds.xform(folGroup, a=True, ws=True, t=folPos)
			cmds.xform(folGroup, a=True ,ws=True, ro=folRot)
			self.follicleJntList.append(folJoint)
			self.follicleGrpList.append(folGroup)
			cmds.parent(folGroup, follicle)

		#now create the control structure for the ribbon
		# basePosRaw = cmds.xform(self.follicleJntList[0], ws=True, q=True, t=True)
		# topPosRaw = cmds.xform(self.follicleJntList[self.numJoints], ws=True, q=True, t=True)
		# baseVec = om.MVector(basePosRaw[0], basePosRaw[1], basePosRaw[2])
		# topVec = om.MVector(topPosRaw[0], topPosRaw[1], topPosRaw[2])

		#find the center position
		ratio = self.centerPos #number 0-1, .5 is the middle

#---------------- now just need to feed adjusted uv pos of mid into "alignToUV"
#---------------- here i should align each top, mid, end to the UV pos I want. . .
		midUV = 0.5 * 2 * ratio

		#create ctrl structure
		prefixList = ["base", "mid", "top"]
		uvList = [0.0, midUV, 1.0]
		groupList = []
		# vecList = [baseVec, midVec, topVec]
		locList = []
		upLocList = []
		ctrlList = []
		ctrlJntList = []

#-----------create some options with switches for how things aim, etc at each other
#--------deal with axis stuff below
#-------then down below we need to use object space to move the locators
#--------below must figure out how to parent the up locs to controls? ???
		#for each of "base", "mid", "top" create the control structure
		for i in range(3):
			groupName = "%s_%s_GRP"%(self.name, prefixList[i])
			groupList.append(groupName)

			# vecName = "%sVec"%prefixList[i]
			# vecList.append(vecName)
#----------------create the whole setup at 000, then align the top group
			#create group
			cmds.group(empty=True, n=groupName)

			thisPos = cmds.xform(groupName, ws=True, q=True, t=True)

			#create and parent constraint locator
			locName = "%s_%s_constr_LOC"%(self.name, prefixList[i])
			locList.append(locName)

			cmds.spaceLocator(n=locName)
			cmds.xform(locName, ws=True, t=(thisPos[0], thisPos[1], thisPos[2]))

			cmds.parent(locName, groupName)

			#create a parent constraint locator under the aim locator

			#create up locator
			upLocName = "%s_%s_up_LOC"%(self.name, prefixList[i])
			upLocList.append(upLocName)

			cmds.spaceLocator(n=upLocName)
			#create option for what direction the up vec is?
#----------------axis here
			cmds.xform(upLocName, ws=True, t=[0,0,-1])
			cmds.parent(upLocName, groupName)

			#create controls
			ctrlName = "%s_%s_CTRL"%(self.name, prefixList[i])
			ctrlList.append(ctrlName)
#----------------axis here
			cmds.circle(nr=(0, 1, 0), r=(self.height/10*3), n=ctrlName)
			cmds.parent(ctrlName, locName)

			#create control joints (will already be parented to ctrl)
			jntName = "%s_%s_ctrl_JNT"%(self.name, prefixList[i])
			ctrlJntList.append(jntName)

			ctrlJoint = cmds.joint(n=jntName, p=(0,0,0))
#----------------axis here
			#align group to surface
			rig.alignToUV(targetObj=groupName, sourceObj=self.ribbonName, sourceU=0.5, sourceV=uvList[i], mainAxis="+z", secAxis="+y", UorV="v")

		#now bind the nurbs geo
		cmds.select(cl=True)

		for jnt in ctrlJntList:
			cmds.select(jnt, add=True)
			cmds.select(self.ribbonName, add=True)

		cmds.skinCluster(mi=3, sw=0.5, omi=True, tsb=True, nw=1)

#-------here add in the constraints to make this work properly. . . on each control have it tell what to aim at? lock these or not (depends on whether it's FK or not?)
#-------also add in the FK option here, too. . .

		#base aim constrain to look at center
		#top aim constrain to look at center
		#mid parent constrain to either?, aim to either, point to either?


		#start packaging stuff up
#-------hide the locators

		folGroup = cmds.group(empty=True, n="%s_follicles_GRP"%self.name)
		for fol in self.follicleList:
			cmds.parent(fol, folGroup)
		cmds.setAttr("%s.inheritsTransform"%folGroup, 0)

		ctrlsGroup = cmds.group(empty=True, n="%s_ctrls_GRP"%self.name)
		for grp in groupList:
			cmds.parent(grp, ctrlsGroup)

		geoGroup = cmds.group(empty=True, n="%s_geo_GRP"%self.name)
		cmds.parent(self.ribbonName, geoGroup)
		cmds.setAttr("%s.inheritsTransform"%geoGroup, 0)

		ribbonGroup = cmds.group(empty=True, n="%s_ribbon_GRP"%self.name)
		cmds.parent(folGroup, ribbonGroup)
		cmds.parent(ctrlsGroup, ribbonGroup)
		cmds.parent(geoGroup, ribbonGroup)

		cmds.select(ribbonGroup)



def ribbon():
	ribbon = RibbonUI()