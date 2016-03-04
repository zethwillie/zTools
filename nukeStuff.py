node = nuke.selectedNode()

for i in range(node.getNumKnobs()):
    print node.knob (i).name()


#sv = node["scene_view"].value()
#print sv

#nuke.nodes.Blur()
nuke.nodes.Blur()

#####-------- how to catch names of the selected nodes (navigation via python)
####----------catch the values of the orig node . . . pass those to the duplicate node

#select the orig then the 'copy' with the updated geo
nodes = nuke.selectedNodes("ReadGeo2")
origVals = nodes[1]["scene_view"].getSelectedItems()
nodes[0]["scene_view"].setSelectedItems(origVals)

#now try to cpy the node, get the path manually THEN copy over the attrs
