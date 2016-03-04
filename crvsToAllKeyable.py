"""grab top node and this will put all crvs under it into allkeyable set"""

import maya.cmds as cmds

mst = cmds.ls(sl=True)[0]

children = cmds.listRelatives(mst, ad=True, s=False)

crvs = []

for chld in children:
    print chld
    if cmds.objectType(chld) == "transform":
        shp = cmds.listRelatives(chld, s=True)
        
        if shp and cmds.objectType(shp[0]) == "nurbsCurve":
            print "--this object is a transform and shape is {}".format(shp[0])
            print "------should be adding to list"
            crvs.append(chld)

for crv in crvs:   
    cmds.sets(crv, e=True, fe="ALLKEYABLE" )
            
