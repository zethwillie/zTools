import zTools.zbw_rigTools as rigT
reload(rigT)

sel = cmds.ls(sl=True)
# maybe a win for name
grp = cmds.group(sel, n="newObj")
cmds.move(0,0,0, grp, rpr=True)
t_orig = cmds.getAttr("{0}.t".format(grp))[0]
t = (t_orig[0]*-1, t_orig[1]*-1, t_orig[2]*-1)

ctrl = rigT.bBox()
print ctrl
newCtrl = cmds.rename(ctrl, "newCtrl")
ctrlGrp = cmds.group(newCtrl, n="newCtrlGrp")

cmds.parent(grp, newCtrl)

cmds.xform(ctrlGrp, a=True, ws=True, t=t)
