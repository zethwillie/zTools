inData = {1:["a", "c", "d"], 2:["b", "d", "e"], 3:["c", "d", "b"], 4:["a", "c", "b", "e"], 5:["c", "e"], 6:["a", "c", "e"], 7:["b", "d", "e"], 8:["a", "b", "c", "e"], 9:["c", "d"], 10:["a", "b", "c","d","e"]}
outSym = [4, 0, 0, 3, 0, 1, 0, 1, 0, 4]

def common_elements(list1, list2):
    resultl = []
    removel = []
    for element in list1:
        if element in list2:
            resultl.append(element)
        else:
            removel.append(element)
    for element in list2:
        if element not in list1:
            removel.append(element)
    return(resultl, removel)


df = zip(inData.keys(), outSym)

objsToOut = []
relObjs = []

for d in df:
    inObjs = []
    if d[1] != 0:
        relObjs.append(inData[d[0]])
        for obj in inData[d[0]]:
            if obj not in inObjs:
                inObjs.append(obj)
    for obj in inObjs:
        if obj not in objsToOut:
            objsToOut.append(obj)

common = relObjs[0]
for l in range(1, len(relObjs)-1):
    addEl, remEl = common_elements(common, relObjs[l+1])
    for x in remEl:
        if x in common:
            common.remove(x)
    
print common


