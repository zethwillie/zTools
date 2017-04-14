import maya.cmds as cmds

sel = cmds.ls(sl=True)
src = sel[0]
tgts = sel[1:]
shps  = cmds.listRelatives(src, s=True)
shp = shps[0]
for shpe in shps:
    if "Deformed" in shpe:
        shp = shpe
hist = cmds.listHistory(shp)
print shp

defs = []
for h in hist:
    types = cmds.nodeType(h, i=True)
    if "geometryFilter" in types and "tweak" not in h:
        defs.append(h)

# here I have to parse the type of deformer and add that
for d in defs:
    typ = cmds.nodeType(d)
    for t in tgts:
        if typ == "cluster":
            # this is weird and hard to do (get cmpts?)
            cmds.cluster(d, e=True, g=t)
        if typ == "nonLinear":
            cmds.nonLinear(d, e=True, g=t)
        if typ == "ffd":
            cmds.lattice(d, e=True, g=t)
