import maya.cmds as cmds

num = 12
sel = cmds.ls(sl=True)

cvs = cmds.ls("{0}.cv[*]".format(sel[0]), fl=True)

length = len(cvs)
xtra = len(cvs)%num

frstVar = xtra/2
secVar = xtra-frstVar

wgtDict = {}

# if the diff is only on or two then add that one to one or both ends. . . ?

cvSel = [cvs[0]]
ind = [0]
for x in range(frstVar, len(cvs), num):
    if cvs[x] not in cvSel:
        cvSel.append(cvs[x])
        ind.append(x)
ind.append(len(cvs)-1)
if cvs[len(cvs)-1] not in cvSel:
    cvSel.append(cvs[len(cvs)-1])

# excluding first and last pts, get pts before (w weight), get pts after (w weight). SHOUDL THIS BE A LIST ALSO? [ptName, wgt]
for y in range(2, len(cvSel)-2):
    diff = ind[y]-ind[y-1]
    unit = 1.0/diff
    tmpCvs = []
    tmpValues = []
    for x in range(diff-1, 0, -1):
        tmpCvs.append(cvs[cvs.index(cvSel[y])-x])
        tmpValues.append(1-(unit*x))

    tmpCvs.append(cvs[y])
    tmpValues.append(1)

    for x in range(1, diff):
        tmpCvs.append(cvs[cvs.index(cvSel[y])+x])
        tmpValues.append(unit*x)

    wgtList = zip(tmpCvs, tmpValues)
    wgtDict[cvs.index(cvSel[y])] = wgtList

addCvs = [cvSel[0], cvSel[1], cvSel[-2], cvSel[-1]]

for y in range(len(addCvs)):
    tmpCvs = []
    tmpValues = []
    
    # get pre- wgts
    if y != 0:
        toCvSelInd = cvSel.index(addCvs[y])
        diff = cvs.index(addCvs[y]) - cvs.index(cvSel[toCvSelInd-1])
        # print "cv:", addCvs[x], "prev:", cvSel[toCvSelInd-1], "diff",diff
        unit = 1.0/diff
        if diff >= 2:
            for x in range(diff-1, 0, -1):
                tmpCvs.append(cvs[cvs.index(addCvs[y])-x])
                tmpValues.append(1-(unit*x))
    
    # add the cv itself and wgt
    tmpCvs.append(addCvs[y])
    tmpValues.append(1)
    
    # get post- wgts
    if y != 3:
        toCvSelInd = cvSel.index(addCvs[y])
        diff = cvs.index(cvSel[toCvSelInd+1]) - cvs.index(addCvs[y])
        unit = 1.0/diff
        if diff >= 2:
            for x in range(1, diff):
                tmpCvs.append(cvs[cvs.index(addCvs[y])+x])
                tmpValues.append(1-(unit*x))

    wgtList = zip(tmpCvs, tmpValues)
    wgtDict[cvs.index(addCvs[y])] = wgtList

cmds.select(cvSel, r=True)

