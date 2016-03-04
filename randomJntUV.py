import maya.cmds as cmds
import random

mf = 5
sel = cmds.ls(sl=True)
num = 5

"""
better then uvs would be to get bounding box of object and divide into chunks
within the chunks get the nearest verts? then carry on? 
Or better to just do something like this in fabric or something to randomly throw darts?
shoot random rays at object? 
number of random joints PER area
"""

def divideUV(divs, *args):
	divSize = 1.0/divs

	uDivs = [divSize*x for x in range(0,divs+1)]
	vDivs = [divSize*x for x in range(0,divs+1)]

	chunks = []

	for x in range(0, len(uDivs)-1):
		chunk = [uDivs[x], uDivs[x+1]]
		chunks.append(chunk)

	return chunks
	
def randInRange(minMax, *args):
	min = minMax[0]
	max = minMax[1]

	randVal= random.uniform(min, max)

	return randVal


def makePosNode(obj, *args):
	posNode = cmds.pointOnSurface("nurbsSphere1", ch=True)

	return posNode

def getWSPtPosition(posNode, uv, *args):
	cmds.setAttr("%s.parameterU"%posNode, uv[0])
	cmds.setAttr("%s.parameterV"%posNode, uv[1])
	pos = cmds.getAttr(posNode + ".position")
	print pos
	return pos

def createJoints(pos, *args):
	pass

def bindJnts(list, obj, *args):
	pass

def randomRotate(obj, *args):
	pass

def randUV(*args):
	for obj in sel:
		print "object = %s"%obj

		chunks = divideUV(num)
		uvs = []
		for x in range(0, len(chunks)):
			for y in range(0, len(chunks)):
				ptx = randInRange(chunks[x])
				pty = randInRange(chunks[y])
				uvs.append([ptx, pty])
		positions = []
		node = makePosNode(obj)
		for uv in uvs:
			pos = getWSPtPosition(node, uv)
			positions.append(pos)
		
		jntList = []
		for pos in positions:
			jnt = createJoints(pos)
			jntList.append(jnt)
		bindJnts(jntList, obj)
		for jnt in jntList:
			randomRotate(jnt)


# for jnt in sel:
# 	randx = random.uniform(-mf,mf)
# 	randy = random.uniform(-mf,mf)
# 	randz = random.uniform(-mf,mf)
	
# 	cmds.xform(jnt, r=True, ro = (randx, randy, randz))

#pointOnSurface - get normal, tan u, tan v - move verts along those axes (CONVERT NORMAL TO A DIRECTION! [COULD BE MOVE OBJ NORMAL*SCALAR])
#moveVertexAlongDirection command