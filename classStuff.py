#example of secretly using things like classes and methods
myString = "thisIsAString"

mySplit = myString.split("IsA")
print mySplit

print(type(myString))

print(type(mySplit))

mySplit.append("OhYeah!")
print(mySplit)

#______________
#example of generic class use
class People(object):
	def __init__(self, first, last, height, salary):
		self.first = first
		self.last = last
		self.height = height
		self.salary = salary

	def info(self):
		print "Employee Info: %s %s:\nHeight: %s inches\nSalary:$%s"%(first, last, height, salary)

#set up two employees
empl01 = People("Zeth", "Willie", "72", "10,000")
empl02 = People("Bamb", "Boozle", "50", "50,000")

#call the method for each instance to print their info
emp01.info()
emp02.info()

#______________
#basic example of using a class to do something in Maya
import maya.cmds as cmds

class GrowingSphere(object):
	def __init__(self):
		self.sphere = cmds.sphere(n="sphere")[0]

	def grow(self):
		scaleX = cmds.getAttr("%s.scaleX"%self.sphere)
		scaleZ = cmds.getAttr("%s.scaleZ"%self.sphere)
		newScaleX = scaleX * 1.5
		newScaleZ = scaleZ * 1.5
		cmds.setAttr("%s.scaleX"%self.sphere, newScaleX)
		cmds.setAttr("%s.scaleZ"%self.sphere, newScaleZ)

testSphere1 = GrowingSphere()
testSphere2 = GrowignSphere()

testSphere1.grow()
testSphere2.grow()

#---------------
#basic use of pymel to show how keeping track of instances can be useful

#this is the python (maya.cmds) way of doing something
import maya.cmds as cmds

pythonSphere = cmds.sphere(n="pythonSphere")
print pythonSphere
print(type(pythonSphere))

#this is the pymel way of doing it
import pymel.core as pm
pymelSphere = pm.sphere(n="pymelSphere")
print pymelSphere
print(type(pymelSphere))

#now try to select them (then change their names and select them)
cmds.select(pythonSphere[0])
pm.select(pymelSphere[0])

#--------------
#a couple of bigger uses of classes in maya
import baseLimb as bl
baseTest = bl.LimbUI()

import armRig as ar
armTest = ar.ArmUI()

import zbw_window as win
winTest = win.Window()

import zbw_ribbon as rib
ribTest = rib.RibbonUI()