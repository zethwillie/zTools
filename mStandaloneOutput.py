print "in the file"
from maya.standalone import initialize, uninitialize
import os
import sys
import maya.cmds as cmds
import maya.mel as mel
print "imported stuff"

#sys.path.append("C:\Program Files\Autodesk\Maya2016\bin\mayapy.exe")
saveout = sys.stdout
fsock = open("c:/Users/zeth/Desktop/zethLog3.log", "w")
sys.stdout = fsock
sys.stderr = fsock

initialize(name="python")
print "initialized python"

cmds.file(force=True, new=True)
cmds.sphere(n="yoSphere")
print "did some maya stuff"

cmds.file(rename="c:/Users/zeth/Desktop/StandaloneFile.ma")
cmds.file(save=True, force=True)
print "saved the scene"

uninitialize()
print "unitialized and out"

sys.stdout = saveout
fsock.close()

