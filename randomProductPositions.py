import maya.cmds as cmds
import random

sel = cmds.ls(sl=True)
master = "GOD"

rot = []
transX = []
transZ = []

for x in range(0,50):
    #create a mult for rotation
    rotMult = cmds.shadingNode("multiplyDivide", asUtility = True, n = "rotMult%s"%x)
    #create a rand value for input 1x 
    cmds.setAttr(rotMult + ".input1X", random.uniform(-1,1))
    #connect master rot to input 2x
    cmds.connectAttr("%s.rotYMult"%master, "%s.input2X"%rotMult)
    #append to list of rot 
    rot.append(rotMult)
    
    #create a mult for x position
    transXMult = cmds.shadingNode("multiplyDivide", asUtility = True, n = "transXMult%s"%x)
    #put rand value in input 1x
    cmds.setAttr(transXMult + ".input1X", random.uniform(-.2,.2))
    #connect master pos x to input 2x
    cmds.connectAttr("%s.transXMult"%master, "%s.input2X"%transXMult)
    #append to list of translate x
    transX.append(transXMult)
    
    #create a mult for z pos
    transZMult = cmds.shadingNode("multiplyDivide", asUtility = True, n = "transZMult%s"%x)
    #put rand value in input 1x
    cmds.setAttr(transZMult + ".input1X", random.uniform(-.2,.2))
    #connect master pos x to input 2x
    cmds.connectAttr("%s.transZMult"%master, "%s.input2X"%transZMult)
    #append to list of translate x
    transZ.append(transZMult)
    
    
#for each obj, connect to random item from list of rot, posx, posz
for obj in sel:
    rand1 = random.randint(0, 49)
    rand2 = random.randint(0, 49)
    rand3 = random.randint(0, 49)
    
    cmds.connectAttr("%s.outputX"%rot[rand1], "%s.ry"%obj)
#for each obj, get offset for postion into addDoubleLinear
    localPos = cmds.xform(obj, q=True, t=True)
    xadd = cmds.shadingNode("addDoubleLinear", asUtility = True, n = obj + "XAdd")
    cmds.setAttr("%s.input1"%xadd, localPos[0])
    cmds.connectAttr("%s.outputX"%transX[rand2], "%s.input2"%xadd)
    cmds.connectAttr("%s.output"%xadd, "%s.tx"%obj)
    
    zadd = cmds.shadingNode("addDoubleLinear", asUtility = True, n = obj + "ZAdd")
    cmds.setAttr("%s.input1"%zadd, localPos[2])
    cmds.connectAttr("%s.outputX"%transZ[rand3], "%s.input2"%zadd)
    cmds.connectAttr("%s.output"%zadd, "%s.tz"%obj)


