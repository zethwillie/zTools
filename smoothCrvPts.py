import maya.cmds as cmds
import maya.OpenMaya as om
import math
"""
smooths a pulled vert based on input number
"""

def getNormalizedTangent(crv):
	"""
	gets normalized tan of selected cv
	"""

	cvs = cmds.ls("{0}.cv[*]".format(crv), fl=True)
	denom = len(cvs)
	
	sel = cmds.ls(sl=True, fl=True)[0]
	
	num = float(sel.partition("[")[2].rpartition("]")[0])
	
	pr = num/denom
	
	tan = cmds.pointOnCurve(crv, pr=pr, nt=True)

	return tan

def lerp(a, b, perc):
	"""pass in a, b as lists[3], perc as 0-1 float"""
	vx = (perc*float(b[0]))+((1-perc)*float(a[0]))
	vy = (perc*float(b[1]))+((1-perc)*float(a[1]))
	vz = (perc*float(b[2]))+((1-perc)*float(a[2]))
	return [vx, vy, vz]
	
tgtPts = cmds.ls(sl=True, fl=True)
numOrig = 100
smooth = .05

for tgtPt in tgtPts:

	tgtPtPos = cmds.pointPosition(tgtPt)
	
	tgtNum = int(tgtPt.partition("[")[2].rpartition("]")[0])
	tgtBase = tgtPt.partition("[")[0]
	crv = tgtBase.partition(".")[0]
	print crv
	tgtTan = getNormalizedTangent(crv)
	
	for x in range(-numOrig, numOrig+1):
		
		if x != 0:
			origPt = "{0}[{1}]".format(tgtBase, tgtNum + x)
			origPtPos = cmds.pointPosition(origPt)
			
			perc = (float(abs(x))/(numOrig + 1.0))
			#print origPt, perc
			
			newPosRaw = om.MVector(*lerp(tgtPtPos, origPtPos, math.sin(perc*3.14*0.5)))
			tan = om.MVector(tgtTan[0]*math.pow(1-perc, 1)*smooth, tgtTan[1]*math.pow(1-perc, 1)*smooth, tgtTan[2]*math.pow(1-perc, 1)*smooth)
			
			if x<0:
				newPos = newPosRaw - tan
			if x>0:
				newPos = newPosRaw + tan
			
			#print origPt, newPosRaw.x, newPosRaw.y, newPosRaw.z
			
			
			cmds.xform(origPt, ws=True, t=newPos)