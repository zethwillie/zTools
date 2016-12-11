import maya.cmds as cmds


widgets = {}

def revFootUI(*args):
    if cmds.window("rfwin", exists = True):
        cmds.deleteUI("rfwin")

    widgets["win"] = cmds.window("rfwin", t="reverse foot temp stuff", w=200, h=200)

    widgets["mCLO"] = cmds.columnLayout(w=200, h=200)

    widgets["ankleTFBG"] = cmds.textFieldButtonGrp()
    widgets["ballTFBG"] = cmds.textFieldButtonGrp()

    


    cmds.showWindow(widgets["win"])


def reverseFoot(*args):
    revFootUI()

# outside and inside controls should be under the ankle (so they don't foollow the toe/ball rolls)

# import maya.cmds as cmds

# sel = cmds.ls(sl=True)

# ankleJnt = sel[0]
# ballJnt = sel[1]
# ballEndJnt = sel[2]

# jnts = [ankleJnt, ballJnt, ballEndJnt]
# poss = []

# for jnt in jnts:
# 	pos = cmds.xform(jnt, q=True, ws=True, rp=True)
# 	poss.append(pos)

# grps = []

# for x in range(0, len(poss)):
# 	grp = cmds.group(empty=True, n=jnts[x]+"_ikgrp")
# 	cmds.xform(grp, ws=True, t=poss[x])
# 	grps.append(grp)
    
# for x in range(len(grps)-1, 0, -1):
# 	cmds.parent(grps[x], grps[x-1])


select ik, ankle, ball, toeEnd
place holders for ankle, ball, toeEnd, inside, outside
Should I create a size holder for the controls? Control for each grp AND attrs on main control?
A generic way to have controls that you can replace? ? ?
# 	