import maya.cmds as cmds
import random

walkList = []
opposite = {"up":"down", "down":"up", "left": "right", "right":"left"}
fullDirs = ["up", "down" , "left", "right"]

def startWalk(levels, *args):
	iters = levels
	origDir = fullDirs[random.randint(0, len(fullDirs)-1)]
	walkList.append(origDir)
	workDirs = cleanDir(fullDirs, origDir)
	#print "\nworkDirs = %s"%workDirs
	while iters >= 2:
		doWalk(workDirs)
		iters = iters - 1

def cleanDir(listy, orig, *args):
	localList = list(listy)
	localList.remove(opposite[orig])
	#print "in cleanDir the list is: %s, the orig is: %s"%(listy, orig)
	return localList

def doWalk(thisList, *args):
	print "thisList is: %s"%thisList
	newDir = random.choice(thisList)
	walkList.append(newDir)
	workDirs = cleanDir(fullDirs, str(newDir))

def walk(num, *args):
	startWalk(num)
	print "final walklist = %s"%walkList
	selectVerts(walkList)

def selectVerts(walklist, *args):
	vertList = []

	sel = cmds.ls(sl=True, fl=True)[0]
	vertList.append(sel)

	for x in range(0, len(walklist)):
		thisv = cmds.pickWalk(d=walklist[x])[0]
		vertList.append(thisv)

	cmds.select(vertList, r=True)

