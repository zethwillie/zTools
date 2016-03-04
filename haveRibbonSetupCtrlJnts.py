import maya.cmds as cmds
import zbw_rig as rig

#already have ribbon with shit-on of joints. Deleted control structure. Create a chain for the master controls
def ctrlSetup():

	cmds.select(hi=True)
	sel = cmds.ls(sl=True)
	ctrlList = []
	groupList = []

	for x in sel:
		if (cmds.listRelatives(x, p=True)):
			cmds.parent(x, w=True)
			#could rename joint here
		ctrl = rig.createControl("%s_CTRL"%x, "cube", "x", "red")
		ctrlList.append(ctrl)
		group = rig.groupOrient(x, ctrl)
		groupList.append(group)
		cmds.parent(x, ctrl)
		
		
	for x in range(len(ctrlList)-1, 0, -1):
		#create a control for the move of the joint
		#snap this to the joint 
		#parent the joint to the control

		#switch this to parenting the new control to the other control . . . 
		cmds.parent(groupList[x], ctrlList[x-1])

		#strip to rotateTranslate, then lock the translate of the old control
		#strip to translate of the new control . . . (lock other channels other than up?2)
		
	#TO-DO----------------put a "local" control onto the joint to do the up/down stuff for each control