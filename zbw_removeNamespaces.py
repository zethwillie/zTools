import maya.cmds as cmds
"""removes namespaces . . . """

rem = ["UI", "shared"]
ns = cmds.namespaceInfo(lon=True, r=True)
for y in rem:
    ns.remove(y)

ns.sort(key = lambda a: a.count(":"), reverse=True)
for n in ns:
    ps = cmds.ls("{}:*".format(n), type="transform")
    for p in ps:
        cmds.rename(p, p.rpartition(":")[2]) 
    cmds.namespace(rm=n)