import maya.cmds as cmds
cmds.colorEditor()
uis = []
#rgbCol =  []
targetWindows = ["MayaWindow"] #'mainWindow', 'graphEditor', 
if cmds.colorEditor(q=1, result=1): 
    rgbCol = cmds.colorEditor(q=1, rgb=1)
    uis = cmds.lsUI(windows=1)
    print uis
for ui in uis:
    if any([t in ui for t in targetWindows]):
        print t
        cmds.window(ui, e=1, bgc=rgbCol)