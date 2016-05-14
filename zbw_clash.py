import maya.cmds as cmds
####### run zbw_clash.clash(1) to fix clashes, run zbw_clash.clash(0) to just tell you about them

def nameFix(name):
	"""for xforms - this will take a base name (ie.'pCube') and find all instances of that and rename by appending a number, starting with the deepest instances in the DAG hier, so as not to bollocks up the later searches by changing items on top of obj"""
	mayaObjs = cmds.ls(name)
	print "---------\nI'm in nameFix for: {0}, and there are --{1}-- instances of this clash".format(name, len(mayaObjs))
	mayaObjs.sort(key = lambda a: a.count("|"), reverse=True) #this sorts by greatest number of "|"

	if mayaObjs:
		if len(mayaObjs)>1:
			for x in range(0, len(mayaObjs)-1):
				cmds.rename(mayaObjs[x], "{0}_{1}".format(mayaObjs[x].rpartition("|")[2], x))
				print "zbw_clash.nameFix: Changed name of {0} --> {1}".format(mayaObjs[x], "{0}_{1}".format(mayaObjs[x].rpartition("|")[2], x))

def detectClashes(fixClashes = True):
	"""look in the scene and returns a list of names that clash (transform only, as shapes will get taken care of by renaming or another pass of cleaning shapes)"""
	clashingNames = []
	mayaResolvedName = {}
	
	allDagNodes = cmds.ls(dag = 1) #get all dag nodes
	for node in allDagNodes:
		if cmds.objectType(node)=="transform": #only transforms
			if len(node.split("|")) > 1:  # is it a dupe (split by "|")
				clashingNames.append(node.split("|")[-1]) # add it to the list
	
	clashes = set(clashingNames) #get rid of dupes, so only one of each name
	print "\n==========================="	
	print "Clashing objects: {}".format(list(clashes))

	if fixClashes and clashes:
		fixFirstClash(clashes, 0)

	elif clashes and not fixClashes:
		for clash in clashes:
			print "CLASH -->", clash
			print cmds.ls(clash)

	if not clashes:
		cmds.warning("No transform clashes found")

	#return(list(clashes))

def detectShapeClashes(fixClashes = False):
	"""look in the scene and returns a list of shapes that clash. Instances will be skipped (shapes w/ >1 xforms)"""
	clashingNames = []
	mayaResolvedName = {}
	
	allDagNodes = cmds.ls(dag = 1, shapes=True) #get all shapes
	for node in allDagNodes:
		if len(node.split("|")) > 1: # ie. if there are duplicate names
			if len(cmds.listRelatives(node, ap=True))==1: #if shape does NOT have more than 1 parent 
				clashingNames.append(node.split("|")[-1])
			#mayaResolvedName.append(node)
			
	clashes = set(clashingNames)
	print "\n==========================="	
	print "Clashing shapes: {}".format(list(clashes))

	if fixClashes and clashes:
	 	fixFirstClash(clashes, 1)

	if clashes and not fixClashes:
		for clash in clashes:
			print "SHAPE CLASH -->", clash
			print cmds.ls(clash)

	if not clashes:
		cmds.warning("No shape clashes found")

	#return(list(clashes))

def fixFirstClash(clashes, shapes = 0):
	"""takes in list of base names that are clashing (ie. "pSphere1", meaning that there are multiple instances of this name), if there's more than one clash in the list, redo the clash detection to make sure names stay relevant"""

	clashList = list(clashes)

	if shapes == 0:
		nameFix(clashList[0])

		if len(clashList)>1:
			detectClashes()
	
	if shapes:
		nameFix(clashList[0])
		
		if len(clashList)>1:
			detectShapeClashes()

def clash(fixClashes = 1):
	"""launch the clash detecting/fixing. Only argument is whether to fix the clashes or not (1/0)"""

	detectClashes(fixClashes)
	if fixClashes == 1: #if we are fixing things, do one more pass to make sure
		detectClashes(fixClashes)
	
	detectShapeClashes(fixClashes)