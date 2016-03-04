import maya.cmds as cmds

"""testing how to use drag and drop callbacks in a UI"""

widgets= {}

def UI(*args):
    if cmds.window("window", exists = True):
        cmds.deleteUI("window")
        
    widgets["win"] = cmds.window("window", t="dragDropwin", w=200, h=100)
    widgets["mainCLO"] = cmds.columnLayout(rs=10)
    widgets["topFLO"]= cmds.formLayout(w=200, h = 200)
    
    widgets["image"] = cmds.image(image = "testImage.jpeg")
    widgets["dragDropBut"] = cmds.button(l="dropOnMe!", rs=False, w=100, h=30, dgc = dragCmd, dpc = dropCmd, c=pressed)
    widgets["text"] = cmds.text("sphere", dgc = dragCmd)
    widgets["butText"] = cmds.text("cube", dgc = dragCmd)
    
    cmds.formLayout(widgets["topFLO"], e=True, af = [(widgets["image"], "top", 0), (widgets["image"], "left", 0), (widgets["dragDropBut"], "top", 0), (widgets["dragDropBut"], "left", 0), (widgets["text"], "top", 35), (widgets["text"], "right", 0), (widgets["butText"], "top", 50), (widgets["butText"], "right", 0)])
    
    cmds.showWindow(widgets["win"])
    
def dropCmd(item, target, message, *args):
    print "I've dropped: %s on %s and the message is: %s"%(item, target, message) 
    str = cmds.text(item, q=True, l=True)
    cmds.button(target, e=True, l= str)
    cmd = cmds.text(item, q=True, l=True)
    cmds.button(target, e=True, c = cmd + "()")
    
    
def dragCmd(item, *args):
    print "I've dragged :", item
    
def pressed(*args):
    lab = cmds.button(widgets["dragDropBut"], q=True, l=True)
    print "I pressed the button and it's label is: %s"%lab

def cube(*args):
    cmds.polyCube()
    
def sphere(*args):
    cmds.polySphere()    
    
UI()