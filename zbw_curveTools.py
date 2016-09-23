import maya.cmds as cmds
import maya.OpenMaya as om
import math
from functools import partial

# some tools to work with crvs

#---------------- draw cv, ep curve buttons

#---------------- on rebuild curves options: have checkbox for keep history, keep original
#---------------- button to wire def one curve to another 
#---------------- quick build control rig (using above . . . )

#---------------- use line though object in UI!!!

widgets = {}

def crvToolsUI():
	if cmds.window("crvToolWin", exists = True):
		cmds.deleteUI("crvToolWin")

	width, height = 300, 220
	widgets["win"] = cmds.window("crvToolWin", t="zbw_curveTools", w=width, h=height)
	widgets["CLO"] = cmds.columnLayout()

	# common functions
	widgets["funcsFrLO"] = cmds.frameLayout("Common Curve Functions", w=width, cll=False, bgc = (0, 0, 0))
	widgets["funcsFLO"] = cmds.formLayout(w=width, h= 250, bgc = (.3, .3, .3))
	
	widgets["cvDisplBut"] = cmds.button(l="Toggle CV display on selected crvs!", width = 280, h=35, bgc = (.5, .5, .4), c = toggleDispl)
	widgets["reverseBut"] = cmds.button(l="Reverse Selected Curves!", width = 280, h=35, bgc = (.4, .5, .4), c = reverseCurve)
	widgets["alignAttachBut"] = cmds.button(l="Quick align/attach! (2 selected, move 2nd->1st)", w=280, h=35, bgc = (.5, .5, .4), c= alignAttach)
	widgets["clusterBut"] = cmds.button(l="Cluster Selected Curves!", width = 280, h=35, bgc = (.4, .5, .4), c = clusterCurves)
	widgets["reparaBut"] = cmds.button(l="Reparameterize Selected Crvs to 0-1!", width = 280, h=35, bgc = (.5, .5, .4), c = reparameter)
	widgets["pivStartBut"] = cmds.button(l="Move Pivot to Start!", width = 135, h=35, bgc = (.5, .4, .4), c = partial(movePivot, 0))
	widgets["pivEndBut"] = cmds.button(l="Move Pivot to End!", width = 135, h=35, bgc = (.5, .4, .4), c = partial(movePivot, 1))

	cmds.formLayout(widgets["funcsFLO"], e=True, af = [
		(widgets["cvDisplBut"], "left", 10),
		(widgets["cvDisplBut"], "top", 5),
		(widgets["reverseBut"], "left", 10),
		(widgets["reverseBut"], "top", 45),
		(widgets["alignAttachBut"], "left", 10),
		(widgets["alignAttachBut"], "top", 85),
		(widgets["clusterBut"], "left", 10),
		(widgets["clusterBut"], "top", 125),
		(widgets["reparaBut"], "left", 10),
		(widgets["reparaBut"], "top", 165),		
		(widgets["pivStartBut"], "left", 10),
		(widgets["pivStartBut"], "top", 205),
		(widgets["pivEndBut"], "left", 155),
		(widgets["pivEndBut"], "top", 205),									
		])

	cmds.setParent(widgets["CLO"])
	widgets["rebuildFrLO"] = cmds.frameLayout("Rebuild Curves", w=width, cll=True, cl=False, bgc = (0, 0, 0))
	widgets["rebuildFLO"] = cmds.formLayout(w=width, h=155, bgc = (.3, .3, .3))
	widgets["ptText"] = cmds.text(l = "How to calculate rebuild pt count?")
	widgets["methodRBG"] = cmds.radioButtonGrp(nrb=2, l1="pts/unit", l2="total count", sl = 1, cc = toggleMethod)
	widgets["recoIFBG"] = cmds.intFieldGrp(l="Points/Unit:", nf = 1, cal = [(1, "left"), (2, "left")], v1= 30, en = True, cw=[(1, 70), (2, 50)])
	widgets["totalIFBG"] = cmds.intFieldGrp(l="Total Count:", nf = 1, cal = [(1, "left"), (2, "left")], v1= 1000, en = False, cw=[(1, 70), (2, 50)])	
	widgets["rebuildBut"] = cmds.button(l="Rebuild Curves!", w = 280, h=35, bgc = (.5, .4, .4), c = rebuildCurves)

	cmds.formLayout(widgets["rebuildFLO"], e=True, af = [
		(widgets["ptText"], "left", 10),
		(widgets["ptText"], "top", 5),		
		(widgets["methodRBG"], "left", 10),
		(widgets["methodRBG"], "top", 25),
		(widgets["recoIFBG"], "left", 10),
		(widgets["recoIFBG"], "top", 55),
		(widgets["totalIFBG"], "left", 10),
		(widgets["totalIFBG"], "top", 80),		
		(widgets["rebuildBut"], "left", 10),
		(widgets["rebuildBut"], "top", 110),
		])

	# hammer points
	cmds.setParent(widgets["CLO"])
	widgets["hammerFrLO"] = cmds.frameLayout("Hammer/Smooth Points", w=width, cll=True, cl=False, bgc = (0, 0, 0))
	widgets["hammerFLO"] = cmds.formLayout(w=width,h=90 , bgc = (.3, .3, .3))
	widgets["hammerText"] = cmds.text(l="Move selected points towards surrounding pts", al="left")
	widgets["hammerNumIFG"] = cmds.intFieldGrp(nf = 1, l = "# of sample pts on either side", cal=[(1, "left"), (2, "left")], cw = [(1, 170), (2, 50)], v1=1)
	widgets["hammerBut"] = cmds.button(l="Hammer/Smooth Points!", w = 280, h=35, bgc = (.3, .4, .5), c = doHammer)	
	# create avg cvs functions - find center of cvs and lerp towards them (0-1)

	cmds.formLayout(widgets["hammerFLO"], e=True, af=[
		(widgets["hammerText"], "left", 10),
		(widgets["hammerText"], "top", 5),
		(widgets["hammerNumIFG"], "left", 10),
		(widgets["hammerNumIFG"], "top", 25),
		(widgets["hammerBut"], "left", 10),
		(widgets["hammerBut"], "top", 50),
		])


	# create line
	cmds.setParent(widgets["CLO"])
	widgets["lineFrLO"] = cmds.frameLayout("Create Line", w=width, cll=True, cl=False, bgc = (0, 0, 0))
	widgets["lineFLO"] = cmds.formLayout(w=width,h=90 , bgc = (.3, .3, .3))
	widgets["lineText"] = cmds.text(l="Create a nurbs line along an axis", al="left")
	widgets["lineLenFFG"] = cmds.floatFieldGrp(nf = 1, l = "Length", cal=[(1, "left"), (2,"left")], cw = [(1, 40), (2, 35)], v1=10.0)
	widgets["lineDenFFG"] = cmds.floatFieldGrp(nf = 1, l = "Pts/Unit", cal=[(1, "left"), (2,"left")], cw = [(1, 40), (2, 35)], v1=.5, pre=3)
	widgets["lineAxisRBG"] = cmds.radioButtonGrp(nrb=3, l1="x", l2="y", l3="z", cw = [(1, 35), (2, 35),(3, 35)], sl=1)
	widgets["lineBut"] = cmds.button(l="Create Line!", w = 280, h=35, bgc = (.5, .5, .4), c = createLine)

	cmds.formLayout(widgets["lineFLO"], e=True, af=[
		(widgets["lineText"], "left", 10),
		(widgets["lineText"], "top", 5),
		(widgets["lineLenFFG"], "left", 10),
		(widgets["lineLenFFG"], "top", 25),
		(widgets["lineDenFFG"], "left", 90),
		(widgets["lineDenFFG"], "top", 25),
		(widgets["lineAxisRBG"], "left", 170),
		(widgets["lineAxisRBG"], "top", 25),			
		(widgets["lineBut"], "left", 10),
		(widgets["lineBut"], "top", 50),
		])

	# smooth points
	# cmds.setParent(widgets["CLO"])
	# widgets["smoothFrLO"] = cmds.frameLayout("Smooth Points", w=width, cll=False, cl=True, bgc = (0, 0, 0))
	# widgets["smoothCLO"] = cmds.columnLayout()
	# cmds.separator(h=5)
	# widgets["smthText"] = cmds.text(l="Conform pts position around an extreme pt", al="left")
	# cmds.separator(h=5)
	# widgets["smthNumIFG"] = cmds.intFieldGrp(nf = 1, l = "# of pts on either side", cal=[(1, "left"), (2, "left")], cw = [(1, 170), (2, 50)], v1=5)
	# widgets["smthPushFFG"] = cmds.floatFieldGrp(nf = 1, l = "tangent push amount (+/-0.05ish?)", cal=[(1, "left"), (2, "left")], cw = [(1, 170), (2, 50)], v1=0.05, precision = 3)
	# widgets["smoothBut"] = cmds.button(l="Smooth Points!", w = 300, h=35, bgc = (.5, .5, .4), c = doSmooth)

	cmds.window(widgets["win"], e=True, w=300, resizeToFitChildren = True, sizeable=True)
	cmds.showWindow(widgets["win"])

def curveCheck(obj):
	""" takes object and returns true if it's a curve"""
	shpList = cmds.listRelatives(obj, shapes = True)
	if (not shpList) or (cmds.objectType(shpList[0]) != "nurbsCurve"):
		return False
	else:
		return True

def createLine(*args):
	""" 
	gets info from win to create nurbs curve along an axis
	"""
	axis = cmds.radioButtonGrp(widgets["lineAxisRBG"], q=True, sl=True)
	length = cmds.floatFieldGrp(widgets["lineLenFFG"], q=True, v1=True)
	density = cmds.floatFieldGrp(widgets["lineDenFFG"], q=True, v1=True)

	numCvs = length * density
	if numCvs < 3.0: # curve needs 3 cvs (for 3 dg curve)
		numCvs = 3.0

	cvDist = length/numCvs

	# make a list of pt dist along some axis
	axisList = []
	for x in range(0,int(numCvs)+1):
		axisList.append(x)

	pts = []

	if axis == 1:
		for y in range(0, int(numCvs)+1):
			pt = [axisList[y]*cvDist, 0, 0]
			pts.append(pt)

	if axis == 2:
		for y in range(0, int(numCvs)+1):
			pt = [0, axisList[y]*cvDist, 0]
			pts.append(pt)

	if axis == 3:
		for y in range(0, int(numCvs)+1):
			pt = [0, 0, axisList[y]*cvDist]
			pts.append(pt)			
		
	line = cmds.curve(name = "line_01", d=3, p=pts)
	shp = cmds.listRelatives(line, s=True)[0]
	cmds.rename(shp, "{}Shape".format(line))
	cmds.select(line, r=True)

def movePivot(side, *args):

	check = False	
	sel = cmds.ls(sl=True, exactType = "transform")

	if sel:
		for x in sel:
			check = curveCheck(x)
			if check:
				# get curve info
				pos = cmds.pointOnCurve(x, parameter = side, position = True)
				cmds.xform(x, ws=True, rp=pos)
			else:
				cmds.warning("{} is not a nurbsCurve object. Skipping!".format(x))

def clusterCurves(*args):
	cmds.ClusterCurve()

def reparameter(*args):
	sel = cmds.ls(sl=True, exactType = "transform")

	check = False
	newCrvs = []

	if sel:
		for x in sel:
			check = curveCheck(x)
			if check:
				crv = x
				newCrv = cmds.rebuildCurve(crv, constructionHistory=False, rebuildType = 0, keepControlPoints=True,  keepRange = 0, replaceOriginal=True, name = "{}_RB".format(crv))[0]

			# reconnect parents and children

			else:
				cmds.warning("{} is not a nurbsCurve object. Skipping!".format(x))

	cmds.select(sel, r=True)

def alignAttach(*args):
	# check selection, curves, etc
	sel = cmds.ls(sl=True)
	crv1 = ""
	crv2 = ""

	if sel and len(sel)== 2:
		check1 = curveCheck(sel[0])
		check2 = curveCheck(sel[1])
		if not check1 and check2:
			cmds.warning("you must select two curves!")
			return
	else:
		cmds.warning("you must select two curves!")
		return		

	crv1, crv2 = sel[0], sel[1]
	newCrv = cmds.alignCurve(crv1, crv2, ch=False, replaceOriginal=False, attach=True, keepMultipleKnots=True, positionalContinuityType=2, tangentContinuity=False, curvatureContinuity=False, name = "{}_ATT".format(crv1))
	cmds.setAttr("{}.v".format(crv1), 0)
	cmds.setAttr("{}.v".format(crv2), 0)


def getCurve(*args):
	sel = cmds.ls(sl=True)
	crv = ""

	if sel and len(sel) == 1:
		check = curveCheck(sel[0])
		if not check:
			cmds.warning("Must select one curve object!")
			return
	else:
		cmds.warning("Must select one curve object!")
		return

	crv = sel[0]
	cmds.textFieldButtonGrp(widgets["curveTFBG"], e=True, tx = crv)

def calculatePts(crv, *args):
	"""
	uses the window to get the number of pts that should be in the curve
	"""	
	mode = cmds.radioButtonGrp(widgets["methodRBG"], q=True, sl=True)

	if mode == 1:
		cLen = cmds.arclen(crv, ch=False)
		perUnit = cmds.intFieldGrp(widgets["recoIFBG"], q=True, v1=True)
		total = cLen * perUnit
	if mode == 2:
		total = cmds.intFieldGrp(widgets["totalIFBG"], q=True, v1=True)

	# print "curve =  {0}, total = {1}".format(crv, total)
	return total

def rebuildCurves(*args):
	""" 
		rebuilds selected curves to specs in window
	"""
	sel = cmds.ls(sl=True, exactType = "transform")

	check = False
	newCrvs = []

	if sel:
		for x in sel:
			check = curveCheck(x)

			if check:
				crv = x
				parent = ""
				parList = cmds.listRelatives(crv, parent = True) 
				if parList:
					parent = parList[0]

				num = calculatePts(crv)

				newCrv = cmds.rebuildCurve(crv, rebuildType = 0, spans = num, keepRange = 0, replaceOriginal=False, name = "{}_RB".format(crv))[0]
				newCrvs.append(newCrv)

				if cmds.objExists("crvRebuildOriginals_GRP"):
					if (parent and parent != "crvRebuildOriginals_GRP"):
						cmds.parent(newCrv, parent)
					if parent != "crvRebuildOriginals_GRP":
						cmds.parent(crv, "crvRebuildOriginals_GRP")
					cmds.setAttr("{}.v".format(crv), 0)

				else:
					cmds.group(empty = True, name = "crvRebuildOriginals_GRP")
					if (parent and parent != "crvRebuildOriginals_GRP"):
						cmds.parent(newCrv, parent)
					if parent != "crvRebuildOriginals_GRP":
						cmds.parent(crv, "crvRebuildOriginals_GRP")
					cmds.setAttr("{}.v".format(crv), 0)

			else:
				cmds.warning("{} is not a nurbsCurve object. Skipping!".format(x))

	cmds.select(newCrvs, r=True)

def toggleMethod(*args):
	sel = cmds.radioButtonGrp(widgets["methodRBG"], q=True, sl=True)
	
	if sel == 1:
		cmds.intFieldGrp(widgets["recoIFBG"], e=True, en=True)
		cmds.intFieldGrp(widgets["totalIFBG"], e=True, en=False)

	elif sel == 2:
		cmds.intFieldGrp(widgets["recoIFBG"], e=True, en=False)
		cmds.intFieldGrp(widgets["totalIFBG"], e=True, en=True)

def toggleDispl(*args):
	cmds.toggle(cv=True)

def reverseCurve(*args):
	sel = cmds.ls(sl=True, exactType = "transform")

	check = False

	if sel:
		for x in sel:
			check = curveCheck(x)
			if check:
				cmds.reverseCurve(x, ch=False, replaceOriginal=True)
	else:
		cmds.warning("Must select some curves")
		return

	cmds.select(sel, r=True)

def getNormalizedTangent(pt = ""):
	"""
	gets normalized tan of selected (or given) list of cvs
	"""

	if cmds.objectType(pt) != "nurbsCurve":
		return

	crv = pt.partition(".")[0]
	print pt, crv
	cvs = cmds.ls("{0}.cv[*]".format(crv), fl=True)

	denom = len(cvs)
	num = float(pt.partition("[")[2].rpartition("]")[0])
	pr = num/denom
	
	tan = cmds.pointOnCurve(crv, pr=pr, nt=True)

	return tan

def lerp(a, b, perc):
	"""
	pass in a, b as lists[3], perc as 0-1 float
	"""
	vx = (perc*float(b[0]))+((1-perc)*float(a[0]))
	vy = (perc*float(b[1]))+((1-perc)*float(a[1]))
	vz = (perc*float(b[2]))+((1-perc)*float(a[2]))
	return [vx, vy, vz]

def doSmooth(*args):
	num = cmds.intFieldGrp(widgets["smthNumIFG"], q=True, v1=True)
	push = cmds.floatFieldGrp(widgets["smthPushFFG"], q=True, v1=True)
	smoothPoints(num, push)

def smoothPoints(num = 5, push = 0.05):
	"""
	tries to smooth the surrounding pts around an outlier cv
	num = number of points on either side to affect
	push = amount to push out along tangent
	"""
	tgtPts = cmds.ls(sl=True, fl=True)

	for tgtPt in tgtPts:

		tgtPtPos = cmds.pointPosition(tgtPt)
		
		tgtNum = int(tgtPt.partition("[")[2].rpartition("]")[0])
		tgtBase = tgtPt.partition("[")[0]
		#crv = tgtBase.partition(".")[0]

		tgtTan = getNormalizedTangent(tgtPt)
		
		for x in range(-num, num+1):
			
			if x != 0:
				origPt = "{0}[{1}]".format(tgtBase, tgtNum + x)
				origPtPos = cmds.pointPosition(origPt)
				
				perc = (float(abs(x))/(num + 1.0))
				#print origPt, perc
				
				newPosRaw = om.MVector(*lerp(tgtPtPos, origPtPos, math.sin(perc*3.14*0.5)))
				tan = om.MVector(tgtTan[0]*math.pow(1-perc/num, num)*push, tgtTan[1]*math.pow(1-perc/num, num)*push, tgtTan[2]*math.pow(1-perc/num, num)*push)
				#tan = om.MVector(tgtTan[0]*push, tgtTan[1]*push, tgtTan[2]*push)

				if x<0:
					newPos = newPosRaw + tan
				if x>0:
					newPos = newPosRaw - tan
				
				#print origPt, newPosRaw.x, newPosRaw.y, newPosRaw.z
				
				cmds.xform(origPt, ws=True, t=newPos)

def doHammer(*args):
	num = cmds.intFieldGrp(widgets["hammerNumIFG"], q=True, v1=True)
	hammerPoints(num)

def hammerPoints(neighbors = 3):
	"""
	moves selected cvs to the weighted average of the pts around it [neighbors]
	"""
	tgtPts = cmds.ls(sl=True, fl=True)
#---------------- add in soft selection? 
	if not tgtPts:
		cmds.warning("Select one or more cvs")
		return

	for tgtPt in tgtPts:

		#tgtPtPos = cmds.pointPosition(tgtPt)
		
		tgtNum = int(tgtPt.partition("[")[2].rpartition("]")[0])
		#tgtBase = tgtPt.partition("[")[0]
		crv = tgtPts[0].partition(".")[0]
		
		ptPosListX = []
		ptPosListY = []
		ptPosListZ = []
		
		count = 0
		
		for x in range(-neighbors, neighbors+1):
			
			count += abs(x)
			
			if x != 0:
				origPt = "{0}.cv[{1}]".format(crv, tgtNum + x)
				origPtPos = cmds.pointPosition(origPt)
				
				for a in range(abs(x)):
					ptPosListX.append(origPtPos[0])
					ptPosListY.append(origPtPos[1])
					ptPosListZ.append(origPtPos[2])
				
		avgX = sum(ptPosListX)/(len(ptPosListX))
		avgY = sum(ptPosListY)/(len(ptPosListY))
		avgZ = sum(ptPosListZ)/(len(ptPosListZ))
		
		newPos = [avgX, avgY, avgZ]
		
		cmds.xform(tgtPt, ws=True, t=newPos)


def lineThroughObjs(*args):
	"""
	select objs and this will draw a curve through their pivots (in order)
	"""
	sel = cmds.ls(sl=True)
	pts = []

	for obj in sel:
		pos = cmds.xform(obj, q=True, ws=True, rp=True)
		pts.append(pos)
		
	cmds.curve(d=3, ep=pts)

#---------------- option to connect objs to ep's
#---------------- cmds.connectAttr("curveShape1.editPoints[2]", "pSphere3.translate", f=True)


def curveTools():
	crvToolsUI()