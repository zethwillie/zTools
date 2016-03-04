from functools import partial
import maya.cmds as cmds

class Window(object):
	"""create a basic window with room to put more stuff, stuff goes into either common or custom UI methods"""

	def __init__(self):
		####### modify for inheritence ########
		self.windowName = "thisTestWindow"
		self.windowSize = [420, 200]
		self.sizeable = 1

		self.createUI()

	def createUI(self):
		"""creates the UI """

		self.widgets = {}

		width = self.windowSize[0]
		height = self.windowSize[1]

		if (cmds.window("zbw_win", exists=True)):
			cmds.deleteUI("zbw_win")

		self.widgets["window"] = cmds.window("zbw_win", title=self.windowName, w=width, h=height, s=self.sizeable)

		#menus for future
		self.menus()

		cmds.setParent(self.widgets["window"])
		self.widgets['formLO'] = cmds.formLayout(nd=100, w=width)
		# self.widgets["topColumnLO"] = cmds.columnLayout(w=width)
		self.widgets["scrollLO"] = cmds.scrollLayout(vst=10)
		self.widgets["lowColumnLO"] = cmds.columnLayout(w=width)
		cmds.formLayout(self.widgets["formLO"], e=True, attachForm = [(self.widgets["scrollLO"], "top", 0), (self.widgets["scrollLO"], "left", 0), (self.widgets["scrollLO"], 'right', 0), (self.widgets["scrollLO"], 'bottom', 35)])

		self.commonUI()

		self.customUI()

		#get to buttons bit
		cmds.setParent(self.widgets["formLO"])

		butWidth = width/3 - 10

		#add buttons
		self.widgets["applyCloseButton"] = cmds.button(w=butWidth, h=30, l='Apply and Close', c=partial(self.action, 1))
		self.widgets["applyButton"] = cmds.button(w=butWidth, h= 30, l='Apply', c=partial(self.action, 0))
		self.widgets['closeButton'] = cmds.button(w=butWidth, h=30, l="close window", c=self.closeWindow)

		cmds.formLayout(self.widgets["formLO"], e=True, attachForm=[(self.widgets["applyCloseButton"], 'bottom', 5), (self.widgets["applyCloseButton"], 'left', 5)])
		cmds.formLayout(self.widgets["formLO"], e=True, attachForm=[(self.widgets["closeButton"], 'bottom', 5), (self.widgets["closeButton"], 'right', 5)])
		cmds.formLayout(self.widgets["formLO"], e=True, attachForm=[(self.widgets["applyButton"], 'bottom', 5)])
		cmds.formLayout(self.widgets["formLO"], e=True, attachControl=[(self.widgets["applyButton"], 'left', 5, self.widgets["applyCloseButton"]),(self.widgets["applyButton"], 'right', 5, self.widgets["closeButton"])])


		cmds.showWindow(self.widgets["window"])
		cmds.window(self.widgets["window"], e=True, w=width, h=height)

	def commonUI(self):
		#########  modify for inheritence ###########
		cmds.text('this is where the common UI elements go')
		cmds.separator(h=100)
		pass

	def customUI(self):
		#########  modify for inheritence ###########
		cmds.text("this is where the custom UI elements go")
		cmds.separator(h=200)
		pass

	def action(self, close, *args):
		############ modify for inheritence #############
		#do the action here

		#close window
		if close:
			self.closeWindow()
		pass

	def closeWindow(self, *args):
		cmds.deleteUI(self.widgets["window"])

	def menus(self):
		#########  modify for inheritence ###########
		#self.widgets["testMenu"] = cmds.menu(l="test")
		self.widgets["menu"] = cmds.menuBarLayout()
		self.widgets["menuFile"] = cmds.menu(label="file")
		cmds.menuItem(l='reset values', c=self.resetValues)
		cmds.menuItem(l="save values", c=self.saveValues)
		cmds.menuItem(l="load values", c=self.loadValues)
		self.widgets["menuHelp"] = cmds.menu(l="help")
		cmds.menuItem(l="print help", c=self.printHelp)

	def printHelp(self, *args):
		#########  modify for inheritence ###########
		print("this is your help, yo")

	def resetValues(self, *args):
		#########  modify for inheritence ###########
		print("test values reset")

	def saveValues(self, *args):
		#########  modify for inheritence ###########
		print("test save values")

	def loadValues(self, *args):
		#########  modify for inheritence ###########
		print("test load values")