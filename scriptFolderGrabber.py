import maya.cmds as cmds
import sys
import os
from functools import partial
import maya.mel as mel

widgets = {}
pyCommands = {}

#py dictionary
    #look in dir for zbw_pythonExec.txt
fname = "/Bluearc/HOME/CHRLX/zwillie/maya/2015-x64/scripts/zbw_pythonExec.txt"
for line in open(fname):
    script, cmd = line.split(":")
    pyCommands[script] = cmd



def scripterUI(*args):
    
    if cmds.window("thisWin", exists = True):
        cmds.deleteUI("thisWin")
        
    widgets["win"] = cmds.window("thisWin", t="Scripter", w= 300, h=200)
    widgets["scrollLO"] = cmds.scrollLayout()
    widgets["mainFLO"] = cmds.formLayout(w=300, h=200)
    widgets["mainTLO"] = cmds.tabLayout(w=300, h=200)
    cmds.formLayout(widgets["mainFLO"], e = True, af = [(widgets["mainTLO"], "top", 5), (widgets["mainTLO"], "left", 5), (widgets["mainTLO"], "right", 5), (widgets["mainTLO"], "bottom", 5)])
    
    cmds.windowPref(widgets["win"], w=320, h=240, te=400, le=500)
    cmds.showWindow(widgets["win"])     
    
    scripterMain()

##### only walk down one level from the place we're looking at

def scripterMain(*args):
    usd = cmds.internalVar(usd=True)
    contents = os.walk(usd)

    print "\n"
    
    for level in contents:
        top = level[0]
        topBase = os.path.basename(top)
        if topBase == "":
            topBase = os.path.dirname(top).rpartition("/")[2]
        print "adding tab for: " + topBase + " --> (%s)"%top
        dirs = level[1]
        files = level[2]
        files.sort()
        
        check = [x for x in files if (x.endswith("py") or x.endswith("mel"))]
            
        if check:
            cmds.setParent(widgets["mainTLO"])
            widgets[top + "SLO"] = cmds.scrollLayout(topBase)
            #widgets[top + "CLO"] = cmds.columnLayout()
             
            for fl in files:
                if (fl.rpartition(".")[2]=="py" or fl.rpartition(".")[2] == "mel"):
                    widgets[fl] = cmds.iconTextButton(style="iconAndTextHorizontal", image1 = fl.rpartition(".")[0] + ".png", l=fl, c = partial(executeScript, fl, top))
        
def executeScript(script, dir, *args):
    
    
    if script.endswith("mel"):
        mel.eval(script.rpartition(".")[0])
    elif script.endswith("py"):
        exec(pyCommands[script.rpartition(".")[0]])         
                
def scripter(*args):
    scripterUI()
    
    
scripter()