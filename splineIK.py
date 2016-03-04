import maya.cmds as cmds

#TO-DO----------------create window that will allow to separately grab the IK jnts and the ctrl joints
#TO-DO----------------control joints get identified, make a control for each (import zbw_rig) and parent constr the joints to the controls. Then bind the curve (rename it!) to the control joints. then figure out (parentConstr?) the loc groups to the joints
#TO-DO----------------bind the spline to the control joints
#TO-DO----------------hook up the ik joints to the control setup (parent constraints? )


# one spine gets ik spline and gets bound to control skel
# the dupe spline gets ik handles that are parented under the other spine and locs that 
# point constrain root of bind spine to root of spline ik hierarchy
# dupe curve and one is measure, the other throws out a ratio
# POINT CONSTR each of the rpIK handles instead of parenting them

# could just parent locators to the control skel and then vary the value of the poleVectorConstraint OR do it the way I did before and vary the locators connection. hmmmm


class divineSpline(object):
	def __init__(self):
		super(divineSpline, self).__init__()

		self.bindJnts = []
		self.ikJnts = []
		self.ctrlJnts = []

		self.ikHandles = []
		self.locList = []
		self.groupList = []

		self.curve = ""
		self.ikSplineName = ""

		self.divineSplineUI()

	def divineSplineUI(self):
		widgets = {}
		if cmds.window("splineWin", exists=True):
			cmds.deleteUI("splineWin")
		widgets["win"] = cmds.window("splineWin", t="Spline Maker", w=300, h=200)
		widgets["columnLO"] = cmds.columnLayout()
		widgets["getIKJntsBut"] = cmds.button(l="Select top of spline chain", w= 300, h=50, bgc=(.5, .5, .5), c=splineIK)
		widgets["getCtrlJntsBut"] = cmds.button(l="Select top of control chain", w=300, h=50, bgc = (.5, 0, 0))

		cmds.showWindow(widgets["win"])

	def splineIK(self, *args):
		tempIKJnts = []
		tempBindJnts = []

		#select top joint of chain for IK
		all = cmds.select(hi=True)
		rawJnts = cmds.ls(sl=True, type="joint")

		#rename to "bind"
		for jnt in rawJnts:
			if cmds.listRelatives(jnt, p=True):
				cmds.parent(jnt, w=True)
			thisRaw = cmds.rename(jnt,"bind_%02d_JNT"%(rawJnts.index(jnt)))
			tempBindJnts.append(thisRaw)


		for x in range(len(tempBindJnts)):
			thisIkRaw = cmds.duplicate(tempBindJnts[x])
			newName = "IK_%02d_JNT"%x
			thisIKJnt = cmds.rename(thisIkRaw, newName)
			tempikJnts.append(thisIKJnt)

		for x in range(len(tempBindJnts)-1, 0, -1):
			cmds.parent(tempBindJnts[x], tempBindJnts[x-1])
			cmds.parent(self.tempIKJnts[x], self.tempIKJnts[x-1])

		cmds.select(tempBindJnts[0], hi=True)
		self.bindJnts = cmds.ls(sl=True, l=True)
		cmds.select(self.tempIKJnts[0], hi=True)
		self.ikJnts = cmds.ls(sl=True, l=True)

		#on IK chain create an IKRP on each jnt pointing to the next one down
		for i in range(len(self.bindJnts)-1):
			ikName = "%s_IKHandle"%self.bindJnts[i].rpartition("|")[2]
			cmds.ikHandle(n=ikName, sj=self.bindJnts[i], ee=self.bindJnts[i+1], solver="ikRPsolver" )
			cmds.parent(ikName, self.ikJnts[i+1])
			self.ikHandles.append(ikName)

		#create splineIK on IK jnts
		self.ikSplineName = "ikSplineHandle"
		splineIK = cmds.ikHandle(sol="ikSplineSolver", n=ikSplineName, sj=self.ikJnts[0], ee=self.ikJnts[len(self.ikJnts)-1])
		self.curve = splineIK[2]


		#on each IK joint create a loc and move it off in some direction (relative to the IKRPsolver), hook it to the IK Handle
		for j in range(len(self.ikHandles)):
			locName  = "pv_loc_%02d"%j
			groupName = locName + "_GRP"
			#create locator
			cmds.spaceLocator(n=locName, p=(0,0,0))
			#get joint position
			jntPos = cmds.xform(self.ikJnts[j], ws=True, q=True, rp=True)
			cmds.xform(locName, ws=True, t=[jntPos[0], jntPos[1]-1, jntPos[2]])
			cmds.poleVectorConstraint(locName, self.ikHandles[j])
			self.locList.append(locName)
			#create an empty group and put it at the jntPos
			cmds.group(empty=True, n=groupName)
			self.groupList.append(groupName)
			cmds.xform(groupName, ws=True, t=jntPos)
			#parent the locs to the groups
			cmds.parent(locName, groupName)
			#parent the groups to the self.ikJnts
			cmds.parent(groupName, self.ikJnts[j])

	def controlJoints(self, *args):
		pass
		#do the stuff to the control joints here

	

