import maya.cmds as cmds

#-------could also select edit point????
#-------multiple selection and average uv position? Orrrr option to create multiple UV's, one on each vertex
#-------grab an edge and convert to 2 verts and get average. . .
#-------have option for distributed (select 2 verts and number of follicles, spread that num between the two uv positions)

#get vertex
vertex = cmds.ls(sl=True, fl=True)
#------check what type of selection you have and convert it to verts

#-------for loop here. . . .
#convert vertex to uvs
uvs = cmds.polyListComponentConversion(fv=True, tuv=True)
#flatten the uv to list and grab first (cuz verts can be multiple uv's)
uv = cmds.ls(uv, fl=True)[0]

#select our uv
cmds.select(uv, r=True)
#convert the uv index to u and v values
uvVal = cmds.polyEditUV(q=True)
cmds.select(vertex)
return(uvVal)