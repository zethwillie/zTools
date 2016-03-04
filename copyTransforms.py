#TO-DO----------------create UI. . . (this is already done, btw)
#TO-DO----------------options for showing values captured, for copying only selected attr. .. for multiple keys? ?
#TO-DO----------------copy and store? or copy from the object at that frame (other object?
import maya.cmds as cmds

sel = cmds.ls(sl=True, type="transform")
if (len(sel)) > 1:
    base = sel[0]

    objs = sel[1:]

    #get transforms
    pos = cmds.getAttr("%s.translate"%base)
    rot = cmds.getAttr("%s.rotate"%base)
    scale = cmds.getAttr("%s.scale"%base)

    #put transforms
    for obj in objs:
        cmds.setAttr("%s.translate"%obj, pos[0][0], pos[0][1], pos[0][2])
        cmds.setAttr("%s.rotate"%obj, rot[0][0], rot[0][1], rot[0][2])
        cmds.setAttr("%s.scale"%obj, scale[0][1], scale[0][1], scale[0][2])

else:
    cmds.warning("Must select more than one object!")