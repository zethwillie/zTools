import maya.cmds as cmds

sel = cmds.ls(sl=True, l=True)
print sel

"""
------need to remove ALL namespaces
------create a UI to select namespaces and remove them from the object?
------or have a separate proc to select the top node and figure out the namespace from that and autoremove it? would be a problem wiht parented stuff?
------orrrrrrr just grab ALL the namespaces in the scene and remove them from our selections

this was idea, but won't work for long names. . .
for thing in sel:
	ns = thing.rpartition(":")[2]
	if ns:
		print ns
	else: 
		print "none" #(this would become a "break"?how to break out of while loop)
"""