"""referencing stuff"""

import maya.cmds as cmds

#ref = cmds.file(r"//Bluearc/HOME/CHRLX/zwillie/Windows/Desktop/deleteMe2.ma", q=True, rfn=True)
ref = cmds.ls(type="reference")
print "ref=",ref


################### ---------------
# use these two to pull out the reference node and files for UI
refFile = cmds.file(q=1, r=True)
print "refFile=",refFile

for r in refFile:
	refs = cmds.file(r, q=True, rfn=True, wcn=True)
	print "refs =",refs

