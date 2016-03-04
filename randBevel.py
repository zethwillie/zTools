import maya.cmds as cmds
import random
"""select obj, this will randomly bevel some edges"""


sel = cmds.ls(sl=True)[0]

edges = cmds.ls("%s.e[*]"%sel, fl=True)

bevelList = []

for edge in edges:
    rand = random.uniform(0,1 )
    if rand > 0.6:
        bevelList.append(edge)

cmds.select(cl=True)
cmds.select(bevelList, r=True)

cmds.polyBevel(fraction = .5, offset = .05)       