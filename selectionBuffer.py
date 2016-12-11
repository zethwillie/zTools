import maya.cmds as cmds
"""selection buffer """

widgets = {}
selection = []

def selectionUI(*args):
    #window stuff, two buttons
    if cmds.window("selWin", exists=True):
        cmds.deleteUI("selWin")
        
    widgets["win"] = cmds.window("selWin", t="zbw_selectionBuffer", s=False)
    widgets["mainCLO"] = cmds.columnLayout(bgc = (.8, .8, .8))
    
    widgets["getBut"] = cmds.button(l="Store Selection", bgc = (.5, .5, .9), w=200, h=50, c=grabSel)
    cmds.separator(h=5)
    widgets["checkBut"] = cmds.button(l="Check Stored (in scipt ed.)", bgc = (.5, .5, .5), w=200, h=20, en=False, c=checkSel)
    cmds.separator(h=10)
    widgets["restoreBut"] = cmds.button(l="Restore Selection", bgc = (.5, .8, .5), w=200, h=50, c=restoreSel)
    
    cmds.window(widgets["win"], e=True, w=200, h=135)
    cmds.showWindow(widgets["win"])

def grabSel(*args):
    
    del selection[:]   
      
    sel = cmds.ls(sl=True, fl=True)
    
    for obj in sel:
        selection.append(obj)
    
    if selection:
        cmds.button(widgets["checkBut"], e=True, bgc = (.8, .7, .5),  en = True)
        
    else:
        cmds.button(widgets["checkBut"], e=True, bgc = (.5, .5, .5), en=False)
    
def checkSel(*args):
    print "\n IN THE SELECTION BUFFER:"
    for obj in selection:
        print obj
    
def restoreSel(*args):
    cmds.select(cl=True)
    
    if selection:
        for obj in selection:
            cmds.select(obj, add=True)


def selectionBuffer(*args):
    selectionUI()
    
selectionBuffer()