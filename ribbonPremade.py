import maya.cmds as cmds
import zTools.zbw_rig as rig



def ribbonPremade(numJoints, dir=1, *args):
	
	name = cmds.ls(sl=True)[0]

	factor = 1.0/(numJoints)
	for x in range (numJoints + 1):
		val = x * factor
		print val
		folName = "%s_follicle%s"%(name, x)
		#create a follicle in the right direction
		if dir ==1:
			follicle = rig.follicle(name, folName, val, 0.5)[0]
		else:
			follicle = rig.follicle(name, folName, 0.5, val)[0]

		# follicleList.append(follicle)

		#create joint and parent to follicle
		jointName = "%s_fol%s_JNT"%(name, x)
#---------have to figure out how to orient this correctly (just translate and rotate the joints (or the controls they're under))
		#create joint control? then move the control and the joint under it to the correct rot and pos
		folPos = cmds.xform(follicle, q=True, ws=True, rp=True)
		folRot = cmds.xform(follicle, q=True, ws=True, ro=True)
		cmds.select(cl=True)
		folJoint = cmds.joint(n=jointName, p=(0,0,0))
		ctrl = rig.createControl(name = "{}Ctrl".format(jointName), type = "sphere", color = "red")
		cmds.parent(folJoint, ctrl)
		folGroup = cmds.group(ctrl, n="%s_GRP"%folJoint)	 #this could become control for the joint
		cmds.xform(folGroup, a=True, ws=True, t=folPos)
		cmds.xform(folGroup, a=True ,ws=True, ro=folRot)
		# follicleJntList.append(folJoint)
		# follicleGrpList.append(folGroup)
		cmds.parent(folGroup, follicle)