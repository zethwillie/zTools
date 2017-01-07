# ways to get connection info on objects

x = cmds.listConnections("pCone1", c=True, p=True)
xShp = cmds.listConnections("pConeShape1", c=True, p=True, skipConversionNodes=True)
if xShp:
	for a in range(0, len(xShp), 2):
		print xShp[a]
		print xShp[a+1] 