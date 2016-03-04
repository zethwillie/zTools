########################
#file: zbw_snap.py
#Author: zeth willie
#Contact: zeth@catbuks.com, www.williework.blogspot.com
#Date Modified: 05/02/13
#To Use: type in python window  "import zbw_snap; zbw_snap.snap()"
#Notes/Descriptions: use to simply snap one object to another. Option for translate, rotate or both. Two options for multi-select: either snap all to the first selection or snap the last selection to the average of the first selections
########################

import maya.cmds as cmds

widgets = {}

def snapUI():
    """simple snap UI for snapping"""

    if cmds.window("snapWin", exists=True):
        cmds.deleteUI("snapWin", window=True)
        cmds.windowPref("snapWin", remove=True)

    widgets["win"] = cmds.window("snapWin", t="zbw_snap", w=210, h=100)
    widgets["mainCLO"] = cmds.columnLayout(w=210, h=100)
    cmds.text("Select the target object(s),\nthen the object(s) you want to snap", al="center", w=210)
    cmds.separator(h=5, style="single")
    widgets["cbg"] = cmds.checkBoxGrp(l="Options: ", ncb=2, v1=1, v2=1, l1="Translate", l2="Rotate", cal=[(1,"left"),(2,"left"), (3,"left")], cw=[(1,50),(2,75),(3,75)])
    widgets["avgRBG"] = cmds.radioButtonGrp(nrb=2, l1="Snap all to first", l2="Snap last to avg", cal=[(1,"left"),(2,"left"),(3,"left")], cw=[(1,100),(2,100)],sl=1)
    widgets["rpCB"] = cmds.checkBox(l="Use Pivot To Query Position?", v=1)
    cmds.separator(h=5, style="single")
    widgets["snapButton"] = cmds.button(l="Snap!", w=210, h=30, bgc=(.6,.8,.6), c=snapIt)

    cmds.showWindow(widgets["win"])
    cmds.window(widgets["win"], e=True, w=210, h=100)


def snapIt(*args):
    """does the snapping by xform. Should work with any rotation order, etc"""
    mode = cmds.radioButtonGrp(widgets["avgRBG"], q=True, sl=True)

    translate = cmds.checkBoxGrp(widgets["cbg"], q=True, v1=True)
    rotate = cmds.checkBoxGrp(widgets["cbg"], q=True, v2=True)
    pivot = cmds.checkBox(widgets["rpCB"], q=True, v=True)

    sel = cmds.ls(sl=True)

    if mode==1:

        target = sel[0]
        objects = sel[1:]

        for obj in objects:
            if translate:
                if pivot:
                    targetPos = cmds.xform(target, ws=True, q=True, rp=True)
                else:
                    targetPos = cmds.xform(target, ws=True, q=True, t=True)

                cmds.xform(obj, ws=True, t=targetPos)

            if rotate:
                #get rot order of obj
                tarRot = cmds.xform(target, ws=True, q=True, ro=True)
                objRO = cmds.xform(obj, q=True, roo=True)
                tarRO = cmds.xform(target, q=True, roo=True)
                cmds.xform(obj, roo=tarRO)
                cmds.xform(obj, ws=True, ro=tarRot)
                cmds.xform(obj, roo=objRO, p=True)

        cmds.select(objects)
    else:
        if (len(sel)>=2):
            targets = sel[0:-1]
            object = sel[-1:][0]

            objRO = cmds.xform(object, q=True, roo=True)

            # tarPosList = []
            # tarRotList = []
            txList = []
            tyList = []
            tzList = []
            rxList = []
            ryList = []
            rzList = []
            TX, TY, TZ, RX, RY, RZ = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for tar in targets:
                if pivot:
                    tarPos = cmds.xform(tar, q=True, ws=True, rp=True)
                else:
                    tarPos = cmds.xform(tar, q=True, ws=True, t=True)
                txList.append(tarPos[0])
                tyList.append(tarPos[1])
                tzList.append(tarPos[2])

                #convert it to the rot order of the object
                tarRO = cmds.xform(tar, q=True, roo=True)
                cmds.xform(tar, p=True, roo=objRO)
                #get the rotation
                tarRot = cmds.xform(tar, q=True, ws=True, ro=True)
                rxList.append(tarRot[0])
                ryList.append(tarRot[1])
                rzList.append(tarRot[2])
                #convert it back
                cmds.xform(tar, p=True, roo=tarRO)

            #now average them all
            for tx in txList:
                TX += tx
            for ty in tyList:
                TY += ty
            for tz in tzList:
                TZ += tz
            for rx in rxList:
                RX += rx
            for ry in ryList:
                RY += ry
            for rz in rzList:
                RZ += rz

            avgTx = TX/len(txList)
            avgTy = TY/len(tyList)
            avgTz = TZ/len(tzList)
            avgRx = RX/len(rxList)
            avgRy = RY/len(ryList)
            avgRz = RZ/len(rzList)

            if translate:
                cmds.xform(object, ws=True, t=(avgTx, avgTy,avgTz))
            if rotate:
                cmds.xform(object, ws=True, ro=(avgRx, avgRy, avgRz))

        else:
            cmds.warning("You need to select two objects or more!")

def snap(*args):
    """function to run the script"""

    snapUI()