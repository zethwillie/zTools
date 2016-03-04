#///////////////////////////////////////////////////////////////////////////////////#
#sk_attrShift
#created by: Sean Kealey (skealeye@gmail.com)
#4.15.11
#version: 1.0
#about: shift custom attributes in channel box up/dn
#to use:  select attributes, shift
#to run:  import sk_attrShift as skattr;skattr.sk_attrShiftUI()
#return:  none
#source: none
#********************************************************************#
#notes: -need select and highlight in channel box after shift 
#update history: ----------
#///////////////////////////////////////////////////////////////////////////////////#

'''
INPUT TO RUN TOOL:
import sk_attrShift as skattr
skattr.sk_attrShiftUI()
'''

#module imports
import maya.cmds as mc 
import maya.mel  as mel
import sys

#Classes 
class sk_attrShift_UI_info():
	
	def version(self):
		version = "v.1.0"	
		return version 
	
	def windowName(self):
		windowName = "sk_attrShift"
		return windowName
		
	def ui(self):
		interface = (self.windowName() + "_UI")
		return interface
	
	def height(self):
		height = 43
		return height 
		
	def width(self):
		width = 205 
		return width

#define class instance
winInfo = sk_attrShift_UI_info()

#-----user interface-----
def sk_attrShiftUI():
	#window size 
	width  = winInfo.width()
	height = winInfo.height() 
	mel.eval('python("import sk_attrShift")')
	
	if mc.window(winInfo.ui(),exists=True):
		mc.deleteUI(winInfo.ui(),window=True) 
	   	mc.windowPref(winInfo.ui(),remove=True)
		
	mainWindow = mc.window(winInfo.ui(),title=winInfo.windowName() + '             ' + winInfo.version(),sizeable=1,minimizeButton=0,maximizeButton=0,widthHeight=[width,height])
	formLayout_1 = mc.formLayout(numberOfDivisions=200)
	rowLayout_1  = mc.rowLayout(numberOfColumns = 2)
	button_1 = mc.button(label='UP' ,command='sk_attrShift.sk_attShiftProc(1)',height=40,width=100,backgroundColor=[.5,.5,.5])
	button_2 = mc.button(label='DN' ,command='sk_attrShift.sk_attShiftProc(0)',height=40,width=100,backgroundColor=[.5,.5,.5])
	
    #mc.window(winInfo.ui(),query=True, widthHeight = True)
	mc.showWindow(mainWindow)

#main procedure			
def sk_attShiftProc(mode):
	obj = mc.channelBox('mainChannelBox',q=True,mol=True)
	if obj:
		attr = mc.channelBox('mainChannelBox',q=True,sma=True)
		if attr:
			for eachObj in obj:
				udAttr = mc.listAttr(eachObj,ud=True)
				if not attr[0] in udAttr:
					sys.exit('selected attribute is static and cannot be shifted')
				#temp unlock all user defined attributes
				attrLock = mc.listAttr(eachObj,ud=True,l=True)
				if attrLock:
					for alck in attrLock:
						mc.setAttr(eachObj + '.' + alck,lock=0)
				#shift down
				if mode == 0:
					if len(attr) > 1:
						attr.reverse()
						sort = attr
					if len(attr) == 1:
						sort = attr 
					for i in sort:
						attrLs = mc.listAttr(eachObj,ud=True)
						attrSize = len(attrLs)
						attrPos = attrLs.index(i)
						mc.deleteAttr(eachObj,at=attrLs[attrPos])
						mc.undo()
						for x in range(attrPos+2,attrSize,1):
							mc.deleteAttr(eachObj,at=attrLs[x])
							mc.undo()
				#shift up 
				if mode == 1:
					for i in attr:
						attrLs = mc.listAttr(eachObj,ud=True)
						attrSize = len(attrLs)
						attrPos = attrLs.index(i)
						if attrLs[attrPos-1]:
							mc.deleteAttr(eachObj,at=attrLs[attrPos-1])
							mc.undo()
						for x in range(attrPos+1,attrSize,1):
							mc.deleteAttr(eachObj,at=attrLs[x])
							mc.undo()
				#relock all user defined attributes			
				if attrLock:
					for alck in attrLock:
						mc.setAttr(eachObj + '.' + alck,lock=1)
						


			
