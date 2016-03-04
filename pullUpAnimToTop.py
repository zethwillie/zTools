#script to pull anim from children up to parent (and kill children anim). Currently only rotate, translate

import maya.cmds as cmds

#dummy check for rotate orders. Is there a way to fix that easily if they have different rot orders?
#check to make sure autokey is on? or use setKey for setting keys

rotBuffer = {}
transBuffer = {}

def zbw_getFrameRange():
    startF = cmds.playbackOptions(query=True, min=True)
    endF = cmds.playbackOptions(query=True, max=True)
    return (startF, endF)

def getRot(obj):
	rotateT = cmds.getAttr((obj+ ".rotate")) #gets WS rotation from bottom object
	rotateNew = [rotateT[0][0], rotateT[0][1], rotateT[0][2]]
	currentFrame = int(cmds.currentTime(query=True)) #gets current frame.
	rotBuffer[currentFrame] = rotateNew #adds the key:value for the frame:rotation
	
def getTrans(obj):
	transT = cmds.xform(obj, query=True, t=True, ws=True) #gets translation from bottom obj
	currentFrame = cmds.currentTime(query=True) #gets current frame.
	transBuffer[currentFrame] = transT #adds the key:value for the frame:rotation

sel = cmds.ls(sl=True)

frames = zbw_getFrameRange()
startF = frames[0]
endF = frames[1]
objSize = len(sel)
topObj = sel[objSize-1]
bottomObj = sel[0]
#get key times for each object add those lists together, convert to set to get rid of dupes
#for each object use clean list to eval to get value, put key, value combo into dictionary

#initialize all keys list
allKeys = []

#create redundant list of frames for all objects (allKeys)
for i in range(0, objSize):
    thisKeys = cmds.keyframe(sel[i], query=True, time=(startF,endF), attribute=('tx','ty','tz','rx','ry','rz'))
    allKeys = allKeys + thisKeys

#turn allKeys into set to clean redundancies (keysSet)   
keysSet = set(allKeys)
#turn set back into clean list (keyList)    
keyList=[]
for key in keysSet:
    keyList.append(key)
keyList.sort()

#populate the dictionary with the key values
#!!!!!!do this for EACH OBJECT in the chain? then the getRot bit would have to be getAttr for rotations, not xform, then rot order is issue!!!!!
for thisKey in keyList: 
	cmds.currentTime(thisKey)
    #get rot and translate data and put into rotBuffer and transBuffer, key:value
	getRot(sel[0])
	getTrans(sel[0])

#go through keys of dictionary
for key in keyList:
	objRot = rotBuffer[key]
	objTrans = transBuffer[key]
	cmds.currentTime(key)
	cmds.xform(topObj, ws=True, t=(objTrans[0], objTrans[1], objTrans[2])) #set keys for B on all the frames in keyBuffer to values in keyBuffer
	cmds.xform(topObj, r=True, ws=True, ro=(objRot[0], objRot[1], objRot[2]))

#zero out the two other controls 
for j in range(0,(objSize-1)):
    #do this with keyframe command? so no need for loop
    cmds.keyframe(sel[j], edit=True, valueChange=0, at=('tx','ty','tz','rx','ry','rz'))
    #add the value to the master control (plus initial offset)
