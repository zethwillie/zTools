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


# or . .. not sure which one works
# import maya.cmds as cmds

# defaults = ['UI', 'shared']

# def num_children(ns): #function to used as a sort key
#     return ns.count(':')

# namespaces = [ns for ns in cmds.namespaceInfo(lon=True, r=True) if ns not in defaults]

# namespaces.sort(key=num_children, reverse=True) # reverse the list

# for ns in namespaces:
#     try:
# 	   	#get contents of namespace and move to root namespace
#     	cmds.namespace(mv=[ns, ":"])
    	
#         cmds.namespace(rm=ns)
#     except RuntimeError as e:
#         # namespace isn't empty, so you might not want to kill it?
#         pass