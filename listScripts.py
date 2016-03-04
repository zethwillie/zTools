import maya.cmds as cmds
import maya.mel as mel
import os
import sys

#create a window
widgets = {}

pythonRun = {
"zbw_appendPath": "import zbw_appendPath; zbw_appendPath.appendPath()",
"zbw_wireRig": "import zbw_wireRig; zbw_wireRig.wireRig()",
"zbw_findScript": "import zbw_findScript; zbw_findScript.findScript()",
"zbw_modelSequence": "import zbw_modelSequence; zbw_modelSequence.modelSequence()",
"cvshapeInverter": "import cvshapeinverter; cvshapeinverter.shapeinverter()",
}

for key in pythonRun:
    print pythonRun[key]

def getScriptsUI(*args):
    
    if cmds.window("thisWin", exists = True):
        cmds.deleteUI("thisWin")
    
    widgets["win"] = cmds.window("thisWin", w=300, h=200)
    widgets["mainCLO"] = cmds.columnLayout()
    
    widgets["list"] = cmds.textScrollList(nr=10, w=300, dcc = executeCommand)
    
    widgets["button"] = cmds.button(l="Refresh List!", w=300, h= 30, bgc = (.8, .6, .3), c= getScripts)
    
    cmds.showWindow(widgets["win"])

#populate the list with the contents of the path
def getScripts(*args):
    
    #### here we should search all possible places, create a separate tab for each location (folder name?)
    
    #get the script path
    usd = cmds.internalVar(usd=True)
    print usd
    #get list of files there
    fls = os.listdir(usd)
      
    for fl in fls:
        print fl
        if (fl.rpartition(".")[2] != "pyc") and (fl[-1] != "~"):
            cmds.textScrollList(widgets["list"], e=True, a=fl)
    
def executeCommand(*args):
    item = cmds.textScrollList(widgets["list"], q=True, si=True)[0]
    #### here we should reference a dictionary of scriptName: code to execute script
    if (item.rpartition(".")[2] == "mel"):
        mel.eval(item.rpartition(".")[0])
        
    elif (item.rpartition(".")[2] == "py"):
        exec(pythonRun[item.rpartition(".")[0]])
    
def scriptList(*args):
    getScriptsUI()
    
scriptList()
    