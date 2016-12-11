# mastering window class that will return the options needed

import maya.cmds as cmds

#callback dismiss function to get the values of the stuff inside
class masterAssetUI(object):
	def __init__(self, *args):
		self.dialog = cmds.layoutDialog(ui=self.masterWindow, t= "Mastering Options")
		self.note = ""
		self.delCam = True
		self.delShd = True
		self.mkRig = True

	def getValues(self):
		pass

	def dismissUI(self, *args):
		self.dict = {}
		self.note = cmds.scrollField(self.txt, q=True, tx=True)
		self.dict["note"] = self.note
		cmds.layoutDialog(dismiss = "got it")

	def masterWindow(self):
		form = cmds.setParent(q=True)
		cmds.formLayout(form, e=True, w=300, h=200)
		t1 = cmds.text(l="Mastering Options:")
		
		self.cam = cmds.checkBoxGrp(l="Delete unused cameras?", ncb = 1, cal=[(1, "left"), (2, "left")], cw = [(1, 200),(2, 100)], v1=True)#delete unused cameras?
		self.shd = cmds.checkBoxGrp(l="Delete unused shaders/textures?", ncb = 1, cal=[(1, "left"), (2, "left")], cw = [(1, 200),(2, 100)], v1=True)#delete unused shaders and textures
		self.rig = cmds.checkBoxGrp(l="Create initial rigs? (for first geo only)", ncb = 1, cal=[(1, "left"), (2, "left")], cw = [(1, 200),(2, 100)], v1=True)#create rig WS? 

		t2 = cmds.text(l="Note:")
		self.txt = cmds.scrollField(h=40, tx = "note field", w=300, ww=True)
		#pum = cmds.popupMenu(b=3, p=widgets["noteSF"])
		#cmds.menuItem("yo", p=pum)
	  
		self.but = cmds.button(l="Master Asset!", bgc = (.5, .7, .4), w=300, h=50, c= self.dismissUI)
		
		cmds.formLayout(form, e=True,attachForm = [(t1, "top", 0), (t1, "left", 5), 
		(self.cam, "top", 25), (self.cam, "left", 5), 
		(self.shd, "top", 45), (self.shd, "left", 5),
		(self.rig, "top", 65), (self.rig, "left", 5),
		(t2, "top", 85), (t2, "left", 5), 
		(self.txt, "top", 105), (self.txt, "left", 5),
		(self.but, "top", 155), (self.but, "left", 5),    
		])
		cmds.formLayout(form, e=True, h=200)

options = masterAssetUI()
print options.dict