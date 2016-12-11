import maya.cmds as cmds
 
## Define path to ui file
pathToFile = '<pathToUiFile>'
 
## Load our window and put it into a variable.
qtWin = cmds.loadUI(uiFile=pathToFile)
 
## Open our window
cmds.showWindow(qtWin)
