import sys, os, datetime, getpass
from maya.standalone import initialize, uninitialize
import maya.cmds as cmds

root = os.environ.get("chrlx_3d_root") 
print root
######## ------- check this below. . .
mayascripts_raw = "{}/maya/maya2015/scripts".format(root)
mayascripts = mayascripts_raw.replace("\\", "/")
print "the append path should be: {}".format(mayascripts)
sys.path.append(mayascripts)
import chrlx_pipe.rigSetup as setup
import chrlx_pipe.masterFuncs as mFuncs

def buildInitialRigFiles(asset, assetFolder, *args):
	"""initializes maya standalone and runs the code to setup the rig ws"""

	#set up the log file
	saveout = sys.stdout
	fsock = open("{0}/{1}_masterLog.log".format(assetFolder, asset), "w")
	sys.stdout = fsock
	sys.stderr = fsock
	print getpass.getuser()
	print datetime.datetime.now()

	print "-------starting build of initial rig files------"

	initialize("python")
	print "== initialized python"

	rigWS = "{0}/rig/workshops/{1}_rig_ws_v001.ma".format(assetFolder, asset)
	geoMst = "{0}/geo/{1}_geo.ma".format(assetFolder, asset)
	print "geoMst", geoMst
	#new scene
	cmds.file(new=True, force=True)
	print "== opened new file"
	#ref in geoMaster
	cmds.file(geoMst, reference=True, renamingPrefix = "geo", deferReference = False, loadReferenceDepth="all", ignoreVersion=True)

	#load the refs
	refs =  cmds.file(q=True, r=True)
	for ref in refs:
		refNode = cmds.referenceQuery(ref, rfn=True)
		print "ref node:", refNode
		if cmds.file(rfn=refNode, q=True, dr=True):
			print "def is True!"
			cmds.file(rfn=refNode, lr=True)

	print "== referenced in: {}".format(geoMst)
	#get reffed geo and group it
	reffed = cmds.ls(geometry=True)
	geo = []
	if reffed:
		for r in reffed:
			p = cmds.listRelatives(r, p=True)
			if p:
				geo.append(p[0])

	grp = cmds.group(empty=True, n="refGeo")
	if geo:
		for g in geo:
			try:
				cmds.parent(g, grp)
			except:
				print "had an issue adding {} to the ref group".format(g)
	print "== parented geo into folder and dropped into 'BODY' con"				
	#run rig setup to build sets and controls
	setup.rigSetup()
	print "== built the rig sets and controls (rigSetup)"
	if cmds.objExists("*RIGDATA"):
		dataNode = cmds.ls("*RIGDATA")[0]
		factor = cmds.getAttr("{}.scaleCtrl".format(dataNode))
		#scale controls
		cmds.select(["GOD.cv[*]", "DIRECTION.cv[*]", "BODY.cv[*]"])
		cmds.scale(factor, factor, factor)
		cmds.select(clear=True)
		cmds.delete("*RIGDATA")

	print "== scaled and deleted control template"
	#parent this group under "BODY"
	cmds.parent(grp, "BODY")
	#rename the scene to asset_rig_ws_v001
	cmds.file(rename=rigWS)
	#save scene
	cmds.file(save=True, type = "mayaAscii", force=True)
	print "== renamed and saved as rig WS"

	#now call master rig on this file
	mFuncs.masterAsset(asset, assetFolder, "rig")
	print "== mastered rig file"

	uninitialize()
	return("completed")

	print "== closing socket"
	#close out the log file
	sys.stdout = saveout
	fsock.close()

buildInitialRigFiles(sys.argv[1], sys.argv[2])
