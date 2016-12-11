import sys
import os
root = os.environ.get("chrlx_3d_root") 
print root
mayascripts = "{}/maya/maya2015/scripts".format(root)
sys.path.append(mayascripts)
#print "the append path should be: {}".format(mayascripts)

from maya.standalone import initialize, uninitialize
import maya.cmds as cmds
import maya.mel as mel

import chrlx_pipe.rigSetup as setup

initialize("python")

cmds.file(new=True, f=True)
newName = "STANDALONETEST.ma"
path = os.path.join("H:/Windows/Desktop", newName)
fileName = cmds.file(rename= path)
sphere = cmds.sphere(n="newSphere")
setup.rigSetup()

cmds.parent(sphere, "BODY")
cmds.sets(sphere, include="ALLKEYABLE")

cmds.file(s=True, type="mayaAscii")
print 'done w scene stuff'
uninitialize()



