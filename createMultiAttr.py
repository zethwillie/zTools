cmds.addAttr('pSphere1', shortName='tt', longName='shotRange', at='compound', numberOfChildren=2, multi=True)
cmds.addAttr('pSphere1', longName='shotRangeStart', at='short', parent='shotRange')
cmds.addAttr('pSphere1', longName='shotRangeEnd', at='short', parent='shotRange')