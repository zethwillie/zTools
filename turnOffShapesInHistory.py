
import maya.cmds as cmds


list = cmds.ls(sl = True)


for x in range(0, len(list)):

    cmds.setAttr(list[x] + '.isHistoricallyInteresting', 0)