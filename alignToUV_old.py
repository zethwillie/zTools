import maya.cmds as cmds
import maya.OpenMaya as om
import math

#use the u and v position to position and align an object to that part of the surface

def matSetRow(matrix, row, newVector):
	om.MScriptUtil.setDoubleArray( matrix[row], 0, newVector.x )
	om.MScriptUtil.setDoubleArray( matrix[row], 1, newVector.y )
	om.MScriptUtil.setDoubleArray( matrix[row], 2, newVector.z )

def matSetCell(matrix, row, column, value):
	om.MScriptUtil.setDoubleArray( matrix[row], column, value )

def radsToDegrees(rads):
	return rads * 180.0 / math.pi

def alignToUV(targetObj="none", sourceObj="none", sourceU=0.0, sourceV=0.0, mainAxis="+z", secAxis="+x", UorV="v"):
"""
	inputs should be 1. targetObj 2. sourceObj 3. sourceU 4. sourceV 5. mainAxis(lowerCase, + or -, i.e."-x" 8. secAxis (lowcase, + or -) 7, UorV ("u" or "v" for the direction along surface for the sec axis)
"""

	axisDict = {"+x":(1,0,0), "+y":(0,1,0), "+z":(0,0,1), "-x":(-1,0,0), "-y":(0,-1,0), "-z":(0,0,-1)}

	#Does this create a new node? no To create a node, use the flag "ch=True". That creates a pointOnSurface node
	pos = cmds.pointOnSurface(sourceObj, u=sourceU, v=sourceV, position=True)
	posVec = om.MVector(pos[0], pos[1], pos[2])
	cmds.xform(targetObj, ws=True, t=pos)

	#get tangent in the right direction (u or v), use this as up vector for normal constraint
	#oooorrrrrr be fancy and create a matrix for the axes to use from normal and tans
	tanV = cmds.pointOnSurface(sourceObj, u=sourceU, v=sourceV, tv=True)
	tanU = cmds.pointOnSurface(targetObj, u=sourceU, v=sourceV, tu=True)
	norm = cmds.pointOnSurface(targetObj, u=sourceU, v=sourceV, nn=True)

	#decide where up axis is on normal constraint, u or v tangent
	if UorV == "v":
		wup = tanV
	elif UorV == "u":
		wup = tanU

	#create normal constraint
	nc = cmds.normalConstraint(sourceObj, targetObj, aimVector=axisDict[mainAxis], upVector=axisDict[secAxis], worldUpVector=(wup))
	cmds.delete(nc) #delete constraint

	#-------check that targetObj is a nurbsSurface (later figure out if it's a mesh or surface)

	# pos = cmds.pointOnSurface(targetObj, u=sourceU, v=sourceV, position=True)
	# vPos = om.MVector(pos[0], pos[1], pos[2])

	# tanV = cmds.pointOnSurface(targetObj, u=sourceU, v=sourceV, tv=True)
	# vTanV = om.MVector(tanV[0], tanV[1], tanV[2])

	# tanU = cmds.pointOnSurface(targetObj, u=sourceU, v=sourceV, tu=True)
	# vTanU = om.MVector(tanU[0], tanU[1], tanU[2])

	# norm = cmds.pointOnSurface(targetObj, u=sourceU, v=sourceV, nn=True)
	# vNorm = om.MVector(norm[0], norm[1], norm[2])

	# mat4x4 = om.MMatrix()

	# matSetRow(mat4x4, 0, vTanU)
	# matSetRow(mat4x4, 1, vNorm)
	# matSetRow(mat4x4, 2, vTanV)
	# matSetRow(mat4x4, 3, vPos)
	# matSetCell(mat4x4, 0, 3, 0)
	# matSetCell(mat4x4, 1, 3, 0)
	# matSetCell(mat4x4, 2, 3, 0)
	# matSetCell(mat4x4, 3, 3, 1)

	# mTrans = om.MTransformationMatrix(mat4x4)
	# mEuler = mTrans.eulerRotation()
	# mTranslate = mTrans.getTranslation("kWorld") #need to get MDagPath object for this

	# print "translation = %f, %f, %f"%(mTranslate
	# 	[0], mTranslate[1], mTranslate[2])

	# print "%f %f %f" % (radsToDegrees(mEuler[0]),
	# radsToDegrees(mEuler[1]), radsToDegrees(mEuler[2]))