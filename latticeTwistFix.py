import maya.cmds as cmds

lat  = cmds.ls(sl=True)[0]
latShp = cmds.listRelatives(lat, s=True)[0]
sDivs = cmds.getAttr("%s.sDivisions"%latShp) 
tDivs =  cmds.getAttr("%s.tDivisions"%latShp)
uDivs = cmds.getAttr("%s.uDivisions"%latShp)

numPerSpan = sDivs * uDivs

clsList = []
grpList = []
grp2List = []
upClsList = []
ctrlList = []
addList = []

for u in range(uDivs):
    pts = []
    for t in range(tDivs):
        for s in range(sDivs):
            pt = "%s.pt[%s][%s][%s]"%(lat, s, t, u)
            pts.append(pt)
    clstr = cmds.cluster(pts, n="Clstr%s"%u)
    clsList.append(clstr[1])
    pos = cmds.xform(clstr[1], ws=True, q=True, rp=True)
   
    ctrl = cmds.duplicate("ctrl", n="ctrl%s"%u)[0]
    ctrlList.append(ctrl)
    cmds.addAttr(ctrl, ln="fix",k=True, at="float" )
    
    grp = cmds.group(em=True, n="%sGRP"%clstr[0])
    grpList.append(grp)
        
    add = cmds.shadingNode("addDoubleLinear", asUtility=True, n="%sAdd"%clstr[0])
    addList.append(add)
    cmds.connectAttr("%s.fix"%ctrl, "%s.input1"%add)
    cmds.connectAttr("%s.output"%add, "%s.ry"%grp)
    
    grp2 = cmds.group(em=True, n="%sHierGRP"%clstr[0])
    grp2List.append(grp2)
    cmds.parent(ctrl, grp)
    cmds.parent(grp, grp2)
    #transform grp here
    cmds.xform(grp2, ws=True, t=pos)
    upPts = []
    for t in range(tDivs):
        upPts.append("%s.pt[0][%s][%s]"%(lat, t, u))
    upClstr = cmds.cluster(upPts, n="upClster%s"%u)
    upClsList.append(upClstr[1])
    ###########  here need to get the cross product and orient the cluster (group) to the pts . . .


for x in range(len(clsList)-1, 0, -1):
    aim = cmds.aimConstraint(clsList[x], grp2List[x-1],aim=(0,1,0), u=(1,0,0), wut="object", wuo=upClsList[x])
    cmds.delete(aim)
    cmds.delete(upClsList[x])
    cmds.parent(clsList[x], ctrlList[x])
    cmds.parent(grp2List[x], grp2List[x-1])
    cmds.connectAttr("%s.ry"%grpList[x-1],"%s.input2"%addList[x])
    cmds.setAttr("%s.v"%clsList[x], 0)
    
    ############ here need to connect the clusters together . . . two ctrls for each 1 in hier, one outside (one ctrl drives itself and then the grp above)
    ############ hier control will drive the rotation of all subsequent groups, other one will just control that cluster
####actually- - - get grp - aim constrain it to cluster with two side bits (create above) as up vec, and pointing to NEXT cluster in list
#### dupe grp to create our hierarchy (also maybe add control?)
#### then parent this cluster to grp, delete constraint, delete sideCluster. Then do stuff above !!!!
