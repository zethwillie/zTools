import maya.cmds as cmds

#get the name of the locator
sel = cmds.ls(sl=True, type="transform")[0]
baseLoc = sel.rpartition("_")[0]
locs = cmds.ls(baseLoc + "*", type = "transform")

#print locs

#simplify that name
baseName  = baseLoc.rpartition("_")[0]

#get list of all products with that name 
geoList = []
objs = cmds.ls(baseName+"*", type="transform")
print objs

for obj in objs:
    if cmds.objectType(cmds.listRelatives(obj, shapes=True)[0], isType= "mesh"):
        geoList.append(obj)
        
#print geoList
if cmds.objExists(baseName + "Grp"):
    cmds.confirmDialog(m="These locators seem to have already been done. Continue?", button = ["yes", "no"], cancelButton = "no")        

#create group for all locs
masterGrp = cmds.group(n=baseName + "Grp", em=True)

#for each loc
for loc in locs:
    #get the locnum
    num = loc.rpartition("_")[2]
    #for each loc create group wtih prod name and number
    geoGrp = cmds.group(em=True, n=loc+"GeoGrp")
    pos = cmds.xform(loc, ws=True, q=True, rp=True)
    scl = cmds.xform(loc, q=True, r=True, s=True)
    
    
    for geo in geoList:
        #instance the products
        
        inst = cmds.instance(geo, n="%s%s"%(geo, num))
        cmds.parent(inst, geoGrp)
    
    #move and scale to loc
    cmds.xform(geoGrp, ws=True, t=pos)
    cmds.xform(geoGrp, r=True, s=(scl[0]*1.12 ,scl[1]*1.12, scl[2]*1.12))
    
    #parnet the group to the loc
    cmds.parent(geoGrp, loc)
    
    #parent group to loc name group
    cmds.parent(loc, masterGrp)
    