import maya.cmds as cmds
from functools import partial

widgets = {}
itemList = ["apple", "applePie", "oranges", "pears", "appleCobbler"]

def popupUI(*args):
	if cmds.window("popupWin", exists=True):
		cmds.deleteUI("popupWin")

	widgets["win"] = cmds.window("popupWin", w=200, rtf=True)
	widgets["mainCLO"] = cmds.columnLayout()

	widgets["testTFG"] = cmds.textFieldGrp(l="text:", cw=[(1, 30), (2, 150)], cal=[(1, "left"),(2,"left")])
	widgets["searchPUM"] = cmds.popupMenu(postMenuCommand=populateMenuItems)

	cmds.window(widgets["win"], e=True, w=5, h=5)
	cmds.showWindow(widgets["win"])


def getText(*args):
	currText = cmds.textFieldGrp(widgets["testTFG"], q=True ,tx=True)	
	return(currText)


def returnMatches(currText, theList, *args):
	matches = []
	if currText and len(currText)>3:
		matches = [x for x in theList if currText in x]

	return(matches)


def populateMenuItems(*args):
	t = getText()
	cmds.popupMenu(widgets["searchPUM"], e=True, dai=True)
	matches = []

	if t:
		matches = returnMatches(t, itemList)

	if matches:
		for item in matches:
			cmds.menuItem(p=widgets["searchPUM"], l=item, c=partial(fillText, item))


def fillText(text, *args):
	cmds.textFieldGrp(widgets["testTFG"], e=True, tx=text)


def popupMenuTest():
	popupUI()

