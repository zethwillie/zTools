import maya.cmds as cmds

if cmds.window("win", exists=True):
	cmds.deleteUI("win")
	
win = cmds.window("win", w=100, h=100)

CLO = cmds.columnLayout(w=100, h=100)

TSL = cmds.textScrollList(w=100, h=100)

itemList = ["one", "two", "three"]

for item in itemList:
	cmds.textScrollList(TSL, e=True, a=item)

itList = ["two"]

for it in itList:
	if it in itemList:
		cmds.textScrollList(TSL, e=True, si=it)
		index = cmds.textScrollList(TSL, q=True, sii=True)[0]
		cmds.textScrollList(TSL, e=True, lf=(index, "obliqueLabelFont"))
		cmds.textScrollList(TSL, e=True, da=True)
	
	
cmds.window(win, e=True, w=100, h=100)	
cmds.showWindow(win)