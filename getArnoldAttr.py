"""get arnold attributes!"""
import maya.cmds as cmds
sn = cmds.attributeInfo( inherited=False, short=True, type="aiAOVDriver" )
for s in sn:
    print "defaultArnoldDriver.%s = %s" %( s, cmds.getAttr( "defaultArnoldDriver.%s" % s ) )

# cmds.setAttr("defaultArnoldDriver.ai_translator", "exr", type="string")