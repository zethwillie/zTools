# -*- coding: utf-8 -*-

"""
This script aligns the move or scale pivot to the average normal of selected faces.
    Align Move Pivot -> align the moving pivot
    Align Scale Pivot -> align the scaling pivot
    Additional Fixing -> fix the orientation of the pivot by aligning the tangent Vector
    Align -> Executing the aligning command
    Reset Move Pivot -> reset the moving pivot
    Reset Scale Pivot -> reset the scaling pivot

Copyright (C) 2015  James.N
"""

__author__ = "James.N"

import math
import maya.cmds as cmds
import pymel.core as pm

def getFaceNormals():
    faceList = [pm.MeshFace(res) for res in pm.filterExpand(expand = True, sm = 34)]
    if len(faceList) == 0: cmds.error("no faces selected!")

    norm = pm.dt.Vector()
    for face in faceList: norm += face.getNormal(space = 'world').normal()

    return norm.normal()

def computeFrame(normal, x_axis, y_axis):
    l1 = list(x_axis)+[0.0]
    l2 = list(y_axis)+[0.0]
    l3 = list(normal)+[0.0]
    pos = [0.0,0.0,0.0,1.0]
    matrix = pm.dt.TransformationMatrix(l1, l2, l3, pos)

    eu = matrix.getRotation()
    return (eu.x, eu.y, eu.z)

def alignPivot(move = True, scale = False, fix = False):
    normal = getFaceNormals()

    if fix:
        up = pm.dt.Vector(0.0, 1.0, 0.0)
        if up == normal: up = pm.dt.Vector(1.0, 0.0, 0.0)

        y_axis = normal.cross(up)
        x_axis = y_axis.cross(normal)

        rot = computeFrame(normal, x_axis, y_axis)

    if move:
        if fix:
            cmds.manipMoveContext("Move", edit=True, mode=6, orientAxes=[rot[0], rot[1], rot[2]])
        else:
            cmds.manipMoveContext("Move", edit=True, mode=6, alignAlong=[normal.x, normal.y, normal.z])
    if scale:
        if fix:
            cmds.manipScaleContext("Scale", edit=True, mode=6, orientAxes=[rot[0], rot[1], rot[2]])
        else:
            cmds.manipScaleContext("Scale", edit=True, mode=6, alignAlong=[normal.x, normal.y, normal.z])
    cmds.refresh(currentView=True)

def resetPivot(pivot):
    if pivot == "move":
        cmds.manipMoveContext("Move", edit=True, mode=2, orientAxes=[0.0, 0.0, 0.0])
    else:
        cmds.manipScaleContext("Scale", edit=True, mode=0, orientAxes=[0.0, 0.0, 0.0])


# create UI
class interface(object):
    WINDOW_NAME = "alignPivotMainWindow"

    def __init__(self):
        self.initUI()

    def initUI(self):
        if pm.control(self.WINDOW_NAME, query = True, exists = True): return

        self.window = pm.window(self.WINDOW_NAME, title = "Align Pivot", mxb = False, width = 300, height = 220)
        self.window.setWidthHeight([300,220])
        self.layout = pm.formLayout(nd=100)

        with pm.formLayout(nd = 100) as form:
            self.align_move = pm.checkBox(label = "Align Move Pivot", value = True)
            self.align_scale = pm.checkBox(label = "Align Scale Pivot", value = False)
            form.hDistribute()
            form.attachForm(str(self.align_move), "left", 10)
        self.fixbox = pm.checkBox(label = "Additional Fixing", value = False)
        self.align_button = pm.button(label = "Align", command = self.align)
        self.sep = pm.separator(style = "in")
        self.reset_move = pm.button(label = "Reset Move Pivot", command = self.resetMove)
        self.reset_scale = pm.button(label = "Reset Scale Pivot", command = self.resetScale)

        self.layout.vDistribute(1,1,1.5,0.5,1,1)
        self.layout.attachForm(str(self.fixbox), "left", 12)

        self.window.show()

    def resetMove(self, *args):
        resetPivot("move")

    def resetScale(self, *args):
        resetPivot("scale")

    def align(self, *args):
        alignPivot(move = self.align_move.getValue(), scale = self.align_scale.getValue(), fix = self.fixbox.getValue())