"""script to just buffer(catch) the transform vals of an object. Then push them back to some selected geo
"""

import maya.cmds as cmds

widgets = {}

def transformBufferUI(*args):
    if cmds.window("tbWin", exists=True):
        cmds.deleteUI("tbWin")
    
    widgets["win"] = cmds.window("tbWin", t="zbw_tranformBuffer", s=False, w=200)
    widgets["mainCLO"] = cmds.columnLayout(w=200)

######## ------ checkbox to enable/disable these. . . .

    widgets["trnFFG"] = cmds.floatFieldGrp(l="Trns: ", nf=3, cw=[(1, 50), (2, 50), (3, 50), (4,50)], cal = [(1, "left"), (2, "left"), (3, "left"), (4,"left")])
    widgets["rotFFG"] = cmds.floatFieldGrp(l="Rot: ", nf=3, cw=[(1, 50), (2, 50), (3, 50), (4,50)], cal = [(1, "left"), (2, "left"), (3, "left"), (4,"left")])
    widgets["sclFFG"] = cmds.floatFieldGrp(l="Scl: ", nf=3, cw=[(1, 50), (2, 50), (3, 50), (4,50)],cal = [(1, "left"), (2, "left"), (3, "left"), (4,"left")])

    widgets["getBut"] = cmds.button(l="Catch\nValues", h=50)
    widgets["setBut"] = cmds.button(l="Set\nValues", h=50)

    cmds.window(widgets["win"], e=True, w=200, h=200)
    cmds.showWindow(widgets["win"])
    
def transformBuffer(*args):
    transformBufferUI(*args)