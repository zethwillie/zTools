import maya.cmds as cmds
import zbw_rig as rig

"""select mopath crv, then guide crv and run"""

# get cv lists
# iterate thorugh and cluster matching cvs
# link ctrls to clstrs


def linkTwoCurves(*args):
    
    clusterList = []
    cvsLists = []
    groupList = []

    sel = cmds.ls(sl=True)

    for crv in sel:
        cvs = cmds.ls("%s.cv[*]"%crv, fl=True)
        cvsLists.append(cvs)

    c1 = cvsLists[0]
    c2 = cvsLists[1]

    #check that they're equal
    if len(c1) == len(c2):
        for x in range(len(c1)):
            name = c1[x].split(".")[0] + "Clstr%s"%x
            clstr = cmds.cluster((c1[x], c2[x]), name=name)[1]
            clusterList.append(clstr)
#--------------find some way to orient? 
            cmds.setAttr("%s.visibility"%clstr, 0)

        for x in range(len(clusterList)):
            name = clusterList[x].replace("Clstr", "Ctrl")
            ctrl = rig.createControl(type="sphere", name=name, color="red")
            grp = cmds.group(em=True, name= "%sGrp"%name)
            groupList.append(grp)

            cmds.parent(ctrl, grp)

            pos = cmds.xform(clusterList[x], q=True, ws=True, rp=True)
            rot = cmds.xform(clusterList[x], q=True, ws=True, ro=True)

            cmds.xform(grp, ws=True, t=pos)
            cmds.xform(grp, ws=True, ro=rot)

            cmds.parent(clusterList[x], ctrl)

        msterGrp = cmds.group(em=True, name="%sCtrlGrp"%sel[0])
        cmds.parent(groupList, msterGrp)

    else:
        cmds.warning("dont' have the same # of cvs in curves")

