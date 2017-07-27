import maya.cmds as cmds
import os

def fixPath(path):
	path = path.replace("\\", "/")
	return(path)

inSceneObject = "sphere1"

ws = cmds.workspace(q=True, rootDirectory=True)
pathr = os.path.join(ws, "cache", "alembic", "old", "testAlembicBnd.abc")
path = fixPath(pathr)
print os.path.isfile(path)
cmds.AbcImport(path, ct=inSceneObject)