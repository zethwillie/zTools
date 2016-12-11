import pymel.core as pm
 
class SimpleRivet():
     
    def __init__(self):
        selection = pm.ls(sl=1, fl=1)
 
        if (len(selection) == 2 and isinstance(selection[0], pm.MeshEdge) and isinstance(selection[1], pm.MeshEdge)):
            ## Now both our selections are edges, so let's continue!
             
            self.main = {
                'meshObject' : selection[0].node().getParent(),
                'edgeIndex1' : selection[0].indices()[0],
                'edgeIndex2' : selection[1].indices()[0]
            }        
             
            ## Create all the nodes we'll need for this tool
            self.createNodes()
            ## Connect all our nodes together
            self.createConnections()
            ## Set all Attributes
            self.setAttributes()
        else:
            ## The selection is not two edges, tell them no!
            pm.warning('Please make sure you select two edges only.')
             
 
 
    def setAttributes(self):
        ## Set attributes on our MeshEdgeNodes        
        self.node['meshEdgeNode1'].isHistoricallyInteresting.set(1)
        self.node['meshEdgeNode2'].isHistoricallyInteresting.set(1)
        self.node['meshEdgeNode1'].edgeIndex[0].set(self.main['edgeIndex1'])
        self.node['meshEdgeNode2'].edgeIndex[0].set(self.main['edgeIndex2'])
         
        ## Setup our loft node, caching improved performance alot
        self.node['loftNode'].reverseSurfaceNormals.set(1)
        self.node['loftNode'].inputCurve.set(size=2)
        self.node['loftNode'].uniform.set(True)
        self.node['loftNode'].sectionSpans.set(3)        
        self.node['loftNode'].caching.set(True) 
             
        ## position the surfaceInfoNode in the absolute center position with cacheing
        self.node['ptOnSurfaceIn'].turnOnPercentage.set(True)
        self.node['ptOnSurfaceIn'].parameterU.set(0.5)
        self.node['ptOnSurfaceIn'].parameterV.set(0.5)
        self.node['ptOnSurfaceIn'].caching.set(True)
             
                                 
    def createNodes(self, *args):
        self.node = {
            'meshEdgeNode1'     : pm.createNode('curveFromMeshEdge'),
            'meshEdgeNode2'     : pm.createNode('curveFromMeshEdge'),
            'ptOnSurfaceIn'     : pm.createNode('pointOnSurfaceInfo'),
            'matrixNode'        : pm.createNode('fourByFourMatrix'),
            'decomposeMatrix'   : pm.createNode('decomposeMatrix'),
            'loftNode'          : pm.createNode('loft'),
            'locator'           : pm.createNode('locator')
        }
 
         
 
 
    def createConnections(self, *args):
        ## Connect our main object's (where we selected our edges from) world mesh information
        ## To our inputMesg of our MeshEdgeNode, this matches info to our new curves.   
        self.main['meshObject'].worldMesh.connect(self.node['meshEdgeNode1'].inputMesh)
        self.main['meshObject'].worldMesh.connect(self.node['meshEdgeNode2'].inputMesh)   
        ## Connect both our meshEdgeNodes to our loftNode, this completes our loftNode
        self.node['meshEdgeNode1'].outputCurve.connect(self.node['loftNode'].inputCurve[0])
        self.node['meshEdgeNode2'].outputCurve.connect(self.node['loftNode'].inputCurve[1])
        ## Connect our loftNode Output Sruface information to our ptOnSurface nodes input
        ## This allows us to get the information from this surface and plug it into our 4x4 Matrix  
        self.node['loftNode'].outputSurface.connect(self.node['ptOnSurfaceIn'].inputSurface)
        ## Connect the Normalized Normals (X,Y,Z) to the first row of the 4x4 Matrix Node
        self.node['ptOnSurfaceIn'].normalizedNormalX.connect(self.node['matrixNode'].in00)
        self.node['ptOnSurfaceIn'].normalizedNormalY.connect(self.node['matrixNode'].in01)
        self.node['ptOnSurfaceIn'].normalizedNormalZ.connect(self.node['matrixNode'].in02)
        ## Connect the Normalized TangentU (X,Y,Z) to the second row of the 4x4 Matrix Node
        self.node['ptOnSurfaceIn'].normalizedTangentUX.connect(self.node['matrixNode'].in10)
        self.node['ptOnSurfaceIn'].normalizedTangentUY.connect(self.node['matrixNode'].in11)
        self.node['ptOnSurfaceIn'].normalizedTangentUZ.connect(self.node['matrixNode'].in12)
        ## Connect the Normalized TangentV (X,Y,Z) to the third row of the 4x4 Matrix Node
        self.node['ptOnSurfaceIn'].normalizedTangentVX.connect(self.node['matrixNode'].in20)
        self.node['ptOnSurfaceIn'].normalizedTangentVY.connect(self.node['matrixNode'].in21)
        self.node['ptOnSurfaceIn'].normalizedTangentVZ.connect(self.node['matrixNode'].in22)
        ## Connect the surface positions (X,Y,Z) to the fourth row of the 4x4 Matrix Node
        self.node['ptOnSurfaceIn'].positionX.connect(self.node['matrixNode'].in30)
        self.node['ptOnSurfaceIn'].positionY.connect(self.node['matrixNode'].in31)
        self.node['ptOnSurfaceIn'].positionZ.connect(self.node['matrixNode'].in32)
        ## All of the above will be processed by the decomposed matrix node to output what we need. 
        ## Connect the 4x4 Matrix output to our decompose matrix Input
        self.node['matrixNode'].output.connect(self.node['decomposeMatrix'].inputMatrix)
        ## Now that our decompose matrix node has our correct information, we can connect the  --
        ## rotate and the translate information to our offset locator group node we created earler, We're done!
        self.node['decomposeMatrix'].outputTranslate.connect(self.node['locator'].getParent().translate)
        self.node['decomposeMatrix'].outputRotate.connect(self.node['locator'].getParent().rotate)                                                                                                                            
 
         
SimpleRivet()