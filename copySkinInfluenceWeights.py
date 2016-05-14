import maya.cmds as cmds
import maya.mel as mel
"""select the orig bound mesh, then the new unbound target mesh and run"""


sel = cmds.ls(sl=True)
orig = sel[0]
target = sel[1]

#get orig obj joints
try:
    jnts = cmds.skinCluster(orig, q=True, influence = True)
except:
    cmds.warning("couldn't get skin weights from {}".format(orig))

print jnts

#bind the target with the jnts
try:
    targetClus = cmds.skinCluster(jnts, target, bindMethod=0, skinMethod=0, normalizeWeights=2, maximumInfluences = 3, obeyMaxInfluences=False, tsb=True)[0]
    print targetClus
except:
    cmds.warning("couln't bind to {}".format(target))
        
#get skin clusters
origClus = mel.eval("findRelatedSkinCluster " + orig)

#copy skin weights from orig to target
try:
    cmds.copySkinWeights(ss=origClus, ds=targetClus, noMirror=True, sa="closestPoint", ia="closestJoint")
except:
    cmds.warning("couldn't copy skin weights from {0} to {1}".format(orig, target))