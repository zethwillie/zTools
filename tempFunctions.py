#create a DAG chain from selection
selList = cmds.ls(sl=True)

for i in range(len(selList)-1,0, -1):
	parent = selList[i]
	child = selList[i-1]

	#cmds.parent(child, parent)



#create a joint at each CV on a curve
def jointOnCurve(name="joint",*args):
	crv = cmds.ls(sl=True)[0]

	cvs = cmds.ls("%s.cv[*]"%crv, fl=True)

	for cv in cvs:
		cmds.select(cl=True)
		pp = cmds.pointPosition(cv)
		cmds.joint(p=pp)

