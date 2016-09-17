""" tries to hammer pt towards its's neighbors"""

import maya.cmds as cmds


tgtPts = cmds.ls(sl=True, fl=True)
neighbors = 5

for tgtPt in tgtPts:

	#tgtPtPos = cmds.pointPosition(tgtPt)
	
	tgtNum = int(tgtPt.partition("[")[2].rpartition("]")[0])
	tgtBase = tgtPt.partition("[")[0]
	crv = tgtBase.partition(".")[0]
	
	ptPosListX = []
	ptPosListY = []
	ptPosListZ = []
	
	count = 0
	
	for x in range(-neighbors, neighbors+1):
		
		count += abs(x)
		
		if x != 0:
			origPt = "{0}[{1}]".format(tgtBase, tgtNum + x)
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

			
			
			