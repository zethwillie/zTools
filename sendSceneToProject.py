import maya.cmds as cmds
import chrlx_pipe.chrlxFuncs as cFuncs
from functools import partial
from chrlx import utils
import os

widgets = {}
charList = []
propList = []
setList = []

def sendSceneToProjectUI():
    if cmds.window("ptieWin", exists=True):
        cmds.deleteUI("ptieWin")
        
    widgets["win"] = cmds.window("ptieWin", title="SendSceneToProject", rtf=True)
    widgets["clo"] = cmds.columnLayout()
    
    #try to get the project --> job path
    proj = cmds.workspace(q=True, act=True)
    pm = utils.PathManager(proj)
    jobPath = ""
    if pm.spotSchema == 2:
        jobPath = pm.jobPath

    # get current scene
    curr = ""
    currpath = cmds.file(q=True, sn=True)
    if currpath:
        curr=os.path.basename(currpath).partition(".")[0]
        print "CURR:", curr

    cmds.text("1. Select the job folder that you'd like to\n     send the current open scene to!", al="left")
    cmds.separator(h=10)
    
    widgets["asstTFBG"] = cmds.textFieldButtonGrp(l="Job:", bl="<<<", cw=[(1,30),(2, 150),(3,20)], cal=[(1,"left"),(2,"left"),(3,"left")], tx=jobPath, bc=getProjectFolder)
    cmds.separator(h=5)
    
    cmds.text("2. Name to save file as",al="left")
    widgets["nameTFG"] = cmds.textFieldGrp(l="Name:", cw=[(1,50),(2,170)], cal=[(1,"left"), (2,"left")],tx=curr)
    cmds.separator(h=10)
    
    cmds.text("3. Select the asset to push the file to\n   (will save to ...CHAR/geo/import_export)", al="left")
    widgets["charFLO"] = cmds.frameLayout("characters", bgc=(.3,.3,.3))
    widgets["charTSL"] = cmds.textScrollList(w=220, h=100, bgc = (0,0,0))

    widgets["propFLO"] = cmds.frameLayout("props", bgc=(.3,.3,.3))
    widgets["propTSL"] = cmds.textScrollList(w=220, h=100, bgc = (0,0,0))

    widgets["setFLO"] = cmds.frameLayout("characters", bgc=(.3,.3,.3))
    widgets["setTSL"] = cmds.textScrollList(w=220, h=100, bgc = (0,0,0))
    cmds.separator(h=10)
    
    widgets["impExpBut"] = cmds.button(l="Send to asset import/export!", h=40, bgc=(.5, .7, .5), c=partial(pushToImportExportExecute, "import"))
    # widgets["wipBut"] = cmds.button(l="Send to job sandbox!", h=40, bgc=(.4, .5, .7), c=partial(pushToImportExportExecute, "wip"))
        
    cmds.window(widgets["win"], e=True, w=5, h=5)
    cmds.showWindow(widgets["win"])
    
    pushToImportExportPopulate()


def pushToImportExportPopulate(*args):
    jobFolder = cmds.textFieldButtonGrp(widgets["asstTFBG"], q=True, tx=True)
    assetFolder = os.path.join(jobFolder, "3D_assets")
    
    charList, propList, setList = cFuncs.getProjectAssetList(assetFolder)
    
    for char in charList:
        cmds.textScrollList(widgets["charTSL"], e=True, a=char, sc=partial(clearTSL, ["propTSL", "setTSL"]))
    for prop in propList:
        cmds.textScrollList(widgets["propTSL"], e=True, a=prop, sc=partial(clearTSL, ["charTSL","setTSL"]))
    for set in setList:
        cmds.textScrollList(widgets["setTSL"], e=True, a=set, sc=partial(clearTSL, ["charTSL","propTSL"]))


def getProjectFolder(*args):
    cmds.textScrollList(widgets["charTSL"], e=True, ra=True)
    cmds.textScrollList(widgets["propTSL"], e=True, ra=True)
    cmds.textScrollList(widgets["setTSL"], e=True, ra=True)
    folder = cmds.fileDialog2(fileMode=3, dialogStyle=1)
    if folder:
        path = utils.PathManager(folder[0])
        if path.spotSchema == 2 and (cFuncs.fixPath(path.jobPath) == folder[0]):
            cmds.textFieldButtonGrp(widgets["asstTFBG"], e=True, tx=folder[0])
            pushToImportExportPopulate()
        else:
            cmds.warning("That folder is not a job in the new project schema!")

def pushToImportExportExecute(type, *args):
    if type == "import":
        jobFolder = cmds.textFieldButtonGrp(widgets["asstTFBG"], q=True, tx=True)
        assetFolder = os.path.join(jobFolder, "3D_assets")
            
        char = cmds.textScrollList(widgets["charTSL"], q=True, si=True)
        prop = cmds.textScrollList(widgets["propTSL"], q=True, si=True)
        set = cmds.textScrollList(widgets["setTSL"], q=True, si=True)
        
        name = cmds.textFieldGrp(widgets["nameTFG"], q=True, tx=True)
        impSavePath = ""
        if char:
            impSavePath = cFuncs.fixPath(os.path.join(assetFolder, "characters", char[0], "geo", "import_export", name+".ma"))
        if prop:
            impSavePath = cFuncs.fixPath(os.path.join(assetFolder, "props", prop[0], "geo", "import_export", name+".ma"))
        if set:
            impSavePath = cFuncs.fixPath(os.path.join(assetFolder, "sets", set[0], "geo", "import_export", name+".ma"))
    
        if impSavePath:
            cmds.file(rename=impSavePath)
            cmds.file(save=True, force=True)
            cmds.warning("You're now in: ", impSavePath)
        else:
            cmds.warning("You need to select the asset to send the file to!")

    if type == "wip":
        print "send to wip"

    cmds.deleteUI(widgets["win"])


def clearTSL(TSLlist=[], *args):
    for tsl in TSLlist:
        cmds.textScrollList(widgets[tsl], e=True, da=True)


def sendSceneToProject():
    sendSceneToProjectUI()