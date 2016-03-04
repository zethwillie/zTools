import sys
sys.path.append(r"C:\Program Files\Autodesk\Maya2016\Python\Lib\site-packages")

from os.path import join

from maya.standalone import initialize
import maya.cmds as cmds
import maya.mel as mel

initialize("python")
origPath = "H:/Windows/Desktop/headlessTest.ma"

cmds.file(origPath, open=True)

mySphere = "pSphere1"
cmds.duplicate(mySphere)
cmds.xform(mySphere, ws=True, t=(3, 3, 3))

newName = "NEWTEST.ma"
path = join("H:/Windows/Desktop", newName)
fileName = cmds.file(rename= path)

cmds.file(s=True)
