import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

#----------------option to place your own control somewhere OR have it automatically place on closest point on mesh
#----------------naming conventions for objects and controls (consequently clusters)
#----------------deal with window for this
#TO-DO----------------put it under a follicle (at least option for that)
#auto iterate up the name? by adding _1, etc


def getSoftSelection():
    #Grab the soft selection
    selection = OpenMaya.MSelectionList()
    softSelection = OpenMaya.MRichSelection()
    OpenMaya.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(selection)

    dagPath = OpenMaya.MDagPath()
    component = OpenMaya.MObject()

    # Filter Defeats the purpose of the else statement
    iter = OpenMaya.MItSelectionList( selection,OpenMaya.MFn.kMeshVertComponent )
    elements, weights = [], []
    while not iter.isDone():
        iter.getDagPath( dagPath, component )
        dagPath.pop() #Grab the parent of the shape node
        node = dagPath.fullPathName()
        fnComp = OpenMaya.MFnSingleIndexedComponent(component)
        getWeight = lambda i: fnComp.weight(i).influence() if fnComp.hasWeights() else 1.0

        for i in range(fnComp.elementCount()):
            elements.append('%s.vtx[%i]' % (node, fnComp.element(i)))
            weights.append(getWeight(i))
        iter.next()

    return elements, weights

def softSelectDef(*args):
    """calls on getSoftSelection() to get the weights of the softSelect and then puts it all under a cluster and a control"""

    elements,weights = getSoftSelection()

    print elements
    print weights

    #get transform and mesh
    xform = elements[0].partition(".")[0]
    #maybe here I should check for "orig", etc and exclude them?
    mesh = cmds.listRelatives(xform, f=True, s=True)[0]

    #select each of the points from the list and create a cluster
    cmds.select(cl=True)
    for elem in elements:
        cmds.select(elem, add=True)

    clus = cmds.cluster(relative=True, name="thisCluster")


    for i in range(len(elements)):
        element = elements[i]
        value = weights[i]
        #percent -v 0.5 thisCluster pSphere1.vtx[241] ;
        cmds.percent(clus[0], element,  v=value, )

    #get cluster position
    clusPos = cmds.xform(clus[1], ws=True, q=True, rp=True)

    #create closest point on mesh (surface?) node
    cpomNode = cmds.shadingNode("closestPointOnMesh", asUtility=True, n="tempCPOM")

    #--------------------
    #inputs and outputs for "closestPointOnMesh":

    #inputs:
    #"mesh"->"inputMesh" (mesh node of transform)
    #"clusPos"->"inPosition"
    #"worldMatrix"(transform of object)->"inputMatrix"

    #outputs:
    #"position"->surfacepoint in space
    #"u"->parameter u
    #"v"->parameter v
    #"normal"->normal vector
    #---------------------

    #connect up object to cpom
    cmds.connectAttr("%s.outMesh"%mesh, "%s.inMesh"%cpomNode)
    cmds.setAttr("%s.inPosition"%cpomNode, clusPos[0], clusPos[1], clusPos[2])
    cmds.connectAttr("%s.worldMatrix"%mesh, "%s.inputMatrix"%cpomNode)

    cpomPos = cmds.getAttr("%s.position"%cpomNode)[0]

    #delete cpom node
    cmds.delete(cpomNode)

    #now create a control, orient it to the follicle
    control = "controlName"
    cmds.curve(n=control, d=1, p=[[0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, -0.382683, 0.0], [-0.70710700000000004, -0.70710700000000004, 0.0], [-0.382683, -0.92388000000000003, 0.0], [0.0, -1.0, 0.0], [0.382683, -0.92388000000000003, 0.0], [0.70710700000000004, -0.70710700000000004, 0.0], [0.92388000000000003, -0.382683, 0.0], [1.0, 0.0, 0.0], [0.92388000000000003, 0.382683, 0.0], [0.70710700000000004, 0.70710700000000004, 0.0], [0.382683, 0.92388000000000003, 0.0], [0.0, 1.0, 0.0], [0.0, 0.92388000000000003, 0.382683], [0.0, 0.70710700000000004, 0.70710700000000004], [0.0, 0.382683, 0.92388000000000003], [0.0, 0.0, 1.0], [0.0, -0.382683, 0.92388000000000003], [0.0, -0.70710700000000004, 0.70710700000000004], [0.0, -0.92388000000000003, 0.382683], [0.0, -1.0, 0.0], [0.0, -0.92388000000000003, -0.382683], [0.0, -0.70710700000000004, -0.70710700000000004], [0.0, -0.382683, -0.92388000000000003], [0.0, 0.0, -1.0], [0.0, 0.382683, -0.92388000000000003], [0.0, 0.70710700000000004, -0.70710700000000004], [0.0, 0.92388000000000003, -0.382683], [0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, 0.0, 0.382683], [-0.70710700000000004, 0.0, 0.70710700000000004], [-0.382683, 0.0, 0.92388000000000003], [0.0, 0.0, 1.0], [0.382683, 0.0, 0.92388000000000003], [0.70710700000000004, 0.0, 0.70710700000000004], [0.92388000000000003, 0.0, 0.382683], [1.0, 0.0, 0.0], [0.92388000000000003, 0.0, -0.382683], [0.70710700000000004, 0.0, -0.70710700000000004], [0.382683, 0.0, -0.92388000000000003], [0.0, 0.0, -1.0], [-0.382683, 0.0, -0.92388000000000003], [-0.70710700000000004, 0.0, -0.70710700000000004], [-0.92388000000000003, 0.0, -0.382683], [-1.0, 0.0, 0.0]])
    cmds.select(cl=True)
    shapes = cmds.listRelatives(control, shapes=True)
    for shape in shapes:
        cmds.setAttr("%s.overrideEnabled"%shape, 1)
        cmds.setAttr("%s.overrideColor"%shape, 14)
    controlGrp = cmds.group(control, n="%s_GRP"%control)

    #put the control at the cpomPos
    cmds.xform(controlGrp, ws=True, t=(cpomPos[0],cpomPos[1],cpomPos[2]))

    clusHandShape = cmds.listRelatives(clus[1], s=True)

    # #move the cluster control to the control space (weighted node)
    cmds.cluster(clus[0], e=True, bs=1, wn=(control, control))

    cmds.setAttr("%s.originX"%clusHandShape[0], 0.0)
    cmds.setAttr("%s.originY"%clusHandShape[0], 0.0)
    cmds.setAttr("%s.originZ"%clusHandShape[0], 0.0)

    cmds.delete(clus[1])

    cmds.setAttr("%s.visibility"%clusHandShape[0], 0)