import maya.cmds as cmds
import random 

sel = cmds.ls(sl=True)
mult = "rotMult.outputX"
scale = "CardCtrl.scaleTriggerAngle"
trans = "CardCtrl.randTranslateMult"
rotx = "CardCtrl.randRotX"
roty = "CardCtrl.randRotY"
rotz = "CardCtrl.randRotZ"

for grp in sel:
    #add 3 random value -.5, .5 for translation
    
    #tx = random.uniform(-0.5, 0.5)
    #ty = random.uniform(-0.5, 0.5)  
    #tz = random.uniform(-0.5, 0.5)
    
    #cmds.addAttr(card, ln="dx", at="float", min=-0.5, max=0.5, k=True, dv=tx)
    #cmds.addAttr(card, ln="dy", at="float", min=-0.5, max=0.5, k=True, dv=ty)
    #cmds.addAttr(card, ln="dz", at="float", min=-0.5, max=0.5, k=True, dv=tz)
    
    #pos = cmds.xform(card, q=True, ws=True, rp=True)
    #rot = cmds.xform(card, q=True, ws=True, ro=True)
    
    #topGrp = cmds.group(em=True, n="{}TopGrp".format(card))
    #grp = cmds.group(em=True, n="{}OffsetGrp".format(card))
    #cmds.xform(grp, ws=True, t=pos)
    #cmds.xform(grp, ws=True, ro=rot)
    #cmds.xform(topGrp, ws=True, t=pos)
    #cmds.xform(topGrp, ws=True, ro=rot)
       
    #cmds.parent(card, grp)
    #cmds.parent(grp, topGrp)
    
    #chld = cmds.listRelatives(card, c=True)[0]
    
    #cmds.addAttr(card, ln="rotOffset", k=True, at="float")
    
    #cmds.transformLimits(card, rx=(-180.0, 0.0), erx=(1, 1) )
    
    subGrp = cmds.listRelatives(grp, c=True)[0]
    card = cmds.listRelatives(subGrp, c=True)[0]
    
    #add = cmds.shadingNode("addDoubleLinear", asUtility=True, n="{}Add".format(card))
    #cmds.connectAttr("{}.rotOffset".format(card), "{}.input1".format(add)) 
    #cmds.connectAttr(mult, "{}.input2".format(add))
    #cmds.connectAttr("{}.output".format(add), "{}.rx".format(grp))    
    
    #chanceRoll = random.uniform(0.0, 1)
    
    #if chanceRoll > 0.5:
        #change = random.uniform(-20.0, 20.0)
        #val = cmds.getAttr("{}.rotOffset".format(card))
        #cmds.setAttr("{}.rotOffset".format(card), val + change)
    
    
    #create condition node
    #cond = cmds.shadingNode("condition", asUtility=True, n="{}Cond".format(card))
    #first term = grp.rotatex
    #cmds.connectAttr("{}.rx".format(grp), "{}.firstTerm".format(cond))
    #seconde term = -150.0
    #cmds.connectAttr(scale, "{}.secondTerm".format(cond))
    #greater than
    #cmds.setAttr("{}.operation".format(cond), 2)
    #true - 1, 1, 1
    #cmds.setAttr("{}.colorIfTrueR".format(cond), 1.0)
    #cmds.setAttr("{}.colorIfTrueG".format(cond), 1.0)
    #cmds.setAttr("{}.colorIfTrueB".format(cond), 1.0)
    #false - 0, 0, 0
    #cmds.setAttr("{}.colorIfFalseR".format(cond), 0.0)
    #cmds.setAttr("{}.colorIfFalseG".format(cond), 0.0)
    #cmds.setAttr("{}.colorIfFalseB".format(cond), 0.0)    
    
    #cmds.connectAttr("{}.outColor".format(cond), "{}.scale".format(grp))
    
    #cmds.addAttr(card, ln="rox", at="float", k=True)
    #cmds.addAttr(card, ln="roy", at="float", k=True)    
    #cmds.addAttr(card, ln="roz", at="float", k=True)
    
    randRy = random.uniform(-15, 15)
    randRx = random.uniform(-15, 15)
    randRz = random.uniform(-15, 15)
    
    cmds.setAttr("{}.rox".format(card), randRx)
    cmds.setAttr("{}.roy".format(card), randRy)
    cmds.setAttr("{}.roz".format(card), randRz)
    #rotMult = cmds.shadingNode("multiplyDivide", asUtility = True, n="{}RotMult".format(card))
    #cmds.connectAttr(rotx, "{}.input1X".format(rotMult))
    #cmds.connectAttr(roty, "{}.input1Y".format(rotMult))
    #cmds.connectAttr(rotz, "{}.input1Z".format(rotMult))
    
    #cmds.connectAttr("{}.rox".format(card), "{}.input2X".format(rotMult))
    #cmds.connectAttr("{}.roy".format(card), "{}.input2Y".format(rotMult))
    #cmds.connectAttr("{}.roz".format(card), "{}.input2Z".format(rotMult))
    
    #cmds.connectAttr("{}.output".format(rotMult), "{}.rotate".format(subGrp))
    
    
    
            
    