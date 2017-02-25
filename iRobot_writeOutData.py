import maya.cmds as cmds
import os
import json
import csv
import collections

widgets = {}

def writeOutUI(*args):
    if cmds.window("writeOutWin", exists=True):
        cmds.deleteUI("writeOutWin")

    widgets["win"] = cmds.window("writeOutWin", w=275, t="Write Out Data")
    widgets["clo"] = cmds.columnLayout()

    cmds.text("This assumes the namespace is 'iRobotLawnMower_'\nThis will switch the fps to 20, bake out the data,\nwrite it to desktop, then switch back to 24fps\nClick first button, wait, then second button")
    widgets["nameTFG"] = cmds.textFieldGrp(l="Data File Name", w=275, cal=[(1,"left"),(2,"left")], cw=[(1, 85),(2, 190)])
    cmds.separator(h=5)
    widgets["convertCBG"] = cmds.checkBoxGrp(l="convert to 20fps", v1=1, cal=[(1, "left"),(2, "left")], cw=[(1,100),(2, 175)])
    cmds.separator(h=5)
    widgets["jsonBut"] = cmds.button(l="write json data to desktop", w=275, h=40, c=writeOut)
    cmds.separator(h=5)
    widgets["csvBut"] = cmds.button(l="convert json to csv", w=275, h=40, c=convert_to_csv)


    cmds.window(widgets["win"], e=True, rtf=True, w=5, h=5)
    cmds.showWindow(widgets["win"])


def get_path(*args):
    """just gets a path to the desktop to save the files there (adds the NAME field + '.json')"""
    name = cmds.textFieldGrp(widgets["nameTFG"], q=True, tx=True)
    desktopPathRaw = os.path.join("H:\Windows\Desktop", name+".json")
    desktopPath = fixPath(desktopPathRaw)
    return(desktopPath)    


def writeOut(*args):
    """ writes out the json data as a dict per frame within a dict"""
    convert = cmds.checkBoxGrp(widgets["convertCBG"], q=True, v1=True)
    desktopPath = get_path()
    fr = 24
    # get current framerate
    if convert:
        convert_to_new_fps("20fps")
        fr = 20
    try:
        rangeMin = int(cmds.playbackOptions(q=True, min=True))
        rangeMax = int(cmds.playbackOptions(q=True, max=True))

        allData = {}
        allData["shotInfo"] = []

        for i in range(rangeMin, rangeMax+1):
            frameInfo = {}
            cmds.currentTime(i) 
            
            frameInfo["frameRate"] = fr
            frameInfo["frameNum"] = i
            frameInfo["theta"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.theta")
            frameInfo["rtWheelPosX"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.rtPosX")
            frameInfo["rtWheelPosY"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.rtPosY")
            frameInfo["rtWheelPosZ"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.rtPosZ")
            frameInfo["lfWheelPosX"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.lfPosX")
            frameInfo["lfWheelPosY"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.lfPosY")
            frameInfo["lfWheelPosZ"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.lfPosZ")
            frameInfo["lfRPM"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.lfRPM")
            frameInfo["lfVelocCPF"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.lfVelocCPF")
            frameInfo["lfVelocMPS"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.lfVelocMPS")
            frameInfo["lfAccelMPSS"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.lfAccelMPSS")
            frameInfo["rtRPM"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.rtRPM")
            frameInfo["rtVelocCPF"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.rtVelocCPF")
            frameInfo["rtVelocMPS"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.rtVelocMPS")
            frameInfo["rtAccelMPSS"] = cmds.getAttr("iRobotLawnMower_mstrBodyCtrl.rtAccelMPSS")         
            
            # sortedFrameInfo = collections.OrderedDict(sorted(frameInfo.items()))
            allData["shotInfo"].append(frameInfo)

        with open(desktopPath, "w") as outfile:
            json.dump(allData, outfile, indent=2)
    except Exception as inst:
        cmds.warning("had an issue sending out the data:")
        print inst

    if convert:
        cmds.currentUnit(time="film")


def convert_to_new_fps(val, *args):
    """takes in the string to change scene units of time"""
    cmds.currentUnit(time=val)


def convert_to_csv(*args):
    """converts the file name (from desktop where we svaed it before) to .csv format to read in excel """
    desktopPath = get_path()
    with open(desktopPath, "r") as jsonFile:

        jsonData = json.load(jsonFile)
        shotData = jsonData['shotInfo']

        # open a file for writing
        with open("{0}.{1}".format(desktopPath.rpartition(".")[0], "csv"), 'w') as csvFile:
            # create the csv writer object
            csvwriter = csv.writer(csvFile)
            count = 0
            for frame in shotData:
                sortedFrame = collections.OrderedDict(sorted(frame.items()))
                if count == 0:
                    header = sortedFrame.keys()
                    csvwriter.writerow(header)
                    count += 1
                csvwriter.writerow(sortedFrame.values())


def fixPath(path):
    newPath = path.replace("\\", "/")
    return(newPath)


def iRobot_writeOutData(*args):
    writeOutUI()