#chrlxShotWin

import maya.cmds as cmds
import maya.mel as mel
import os
import chrlx_pipe.chrlxFuncs as cFuncs
reload(cFuncs)
from functools import partial
import chrlx_pipe.projectSetter as projectSetter
import sys
import webbrowser as browser

#a class to store basic variables across functions
class ProjectVars(object):

	def __init__(self):
	#many of these are getting set in the populate window function or the poluateAsset, Shot and updateAssetInfo functions 
		self.currentProject = ""
		self.job = ""
		self.spot = ""
		self.spotRefFolder = ""
		self.charFolder = ""
		self.propFolder = ""
		self.setFolder = ""
		self.shotsFolder = ""
		self.currentAsset = ""
		self.currentAssetFolder = ""
		self.currentGeoFolder = ""
		self.currentRigFolder = ""
		self.currentAssetLatestGeoWS = ""
		self.currentAssetLatestRigWS = ""
		self.currentAssetGeoMaster = ""
		self.currentAssetRigMaster = ""
		self.currentShot = ""
		self.currentShotNum = ""
		self.currentJobNumber = ""
		self.currentShotFolder = ""
		self.currentAnmFolder = ""
		self.currentLgtFolder = ""
		self.currentFxFolder = ""
		self.currentShotLatestAnmWS = ""
		self.currentShotLatestLgtWS = ""
		self.currentShotLatestFXWS = ""
		self.currentShotAnmMaster = ""
		self.currentShotLgtMaster = ""
		self.currentShotFXMaster = ""

		self.openSceneFullPath = ""
		self.openScene = ""
		self.user = mel.eval("getenv USER")
		self.date = ""
		self.time = ""

#dictionary of UI widgets
widgets = {}
pi = ProjectVars()

ann = {"proj":"opens window to set your project - job/spot",
"openAnmWS":"opens the latest WS of the shot selected on the left",
"incrAnmWS":"saves current scene as an incremented version of the shot selected on left",
"prevAnmWS":"opens window to browse prev anim WS's",
"openAnmMst":"opens the published master of the anm shot selected on left",
"pubAnmMst":"opens window to publish the current scene as the anm master for the selected shot",
"prevAnmMst":"opens window to browse previous anim master versions of the selected shot",
}



############
# UI creation
###########

def shotWinUI(*args):
	"""create the UI for the shotWin"""
### ---------- should check for current project
	if cmds.window("shotWin", exists = True):
		cmds.deleteUI("shotWin")

	widgets["win"] = cmds.window("shotWin", t= "Charlex Shot Manager", w=1000, h=560, s=False)
	widgets["mainCLO"] = cmds.columnLayout(w=1000, h=560)

	#######################
	#top bar layout
	#######################

	#rowlayout
	widgets["bannerFLO"] = cmds.formLayout(w=1000, h=50, bgc=(.300,.3,.300))
########### make UI icons & pics relative to env variable!!	
	widgets["bannerImage"] = cmds.image(image="H:/development/3D/maya/maya2015/scripts/chrlx_pipe/images/banner_shotWin.png")
	widgets["projectText"] = cmds.text(l="Project Name: Spot Name", font = "boldLabelFont")
	widgets["sceneText"] = cmds.text(l="Current Scene")	
	widgets["projectButton"] = cmds.button(l="Change Job", w = 100, h= 40, bgc= (.5,.5,.5), ann = ann["proj"], c=setProject)
	widgets["refreshButton"] = cmds.button(l="Refresh", w = 60, h= 40, bgc= (.2,.2,.2), c = populateWindow)
	widgets["exploreButton"] = cmds.button(l="Explore\nReference", w = 60, h= 40, bgc= (.7,.5,.3), c=exploreReference)

	cmds.formLayout(widgets["bannerFLO"], e=True, af = [(widgets["bannerImage"], "top", 0),
		(widgets["bannerImage"], "left", 0),
		(widgets["projectText"], "left", 400),
		(widgets["projectText"], "top", 5),
		(widgets["sceneText"], "top", 25),
		(widgets["sceneText"], "left", 400),
		(widgets["projectButton"], "left", 740),
		(widgets["projectButton"], "top", 5),
		(widgets["refreshButton"], "left", 850),
		(widgets["refreshButton"], "top", 5),
		(widgets["exploreButton"], "left", 920),
		(widgets["exploreButton"], "top", 5),		
		])

		######################
		#bottom layout
		########################
	cmds.setParent(widgets["mainCLO"])
	widgets["lowFLO"] = cmds.formLayout()
	widgets["lowTLO"] = cmds.tabLayout(bgc = (.2, .2, .2 ))

			################
			#shots tab
			################
	cmds.setParent(widgets["lowTLO"])
	widgets["shotsFLO"] = cmds.formLayout("Shots - Anim, Light and FX",w=1000, h=500, bgc = (.4,.4,.4))
	
				##############
				#shot asset List layout
				###############
	widgets["shotAssListCLO"] = cmds.columnLayout(w=240, bgc = (.5, .5,.5))
	widgets["shotAssListFLO"] = cmds.formLayout(w=240, h= 500)
	widgets["shotAssCharListTSL"] = cmds.textScrollList(w=240, h=140)
	widgets["shotAssPropListTSL"] = cmds.textScrollList(w=240, h=140)
	widgets["shotAssSetListTSL"] = cmds.textScrollList(w=240, h=140)
	widgets["shotAssListTitleText"] = cmds.text(l="Assets In Current Scene", font = "boldLabelFont")
	widgets["shotAssListCharText"] = cmds.text(l="Characters")
	widgets["shotAssListPropText"] = cmds.text(l="Props")
	widgets["shotAssListSetText"] = cmds.text(l="Sets")

	cmds.formLayout(widgets["shotAssListFLO"], e=True, af = [
		(widgets["shotAssCharListTSL"], "top", 40), 
		(widgets["shotAssCharListTSL"], "left", 0),
		(widgets["shotAssPropListTSL"], "top", 200),
		(widgets["shotAssPropListTSL"], "left", 0),
		(widgets["shotAssSetListTSL"], "top", 360),
		(widgets["shotAssSetListTSL"], "left", 0),
		(widgets["shotAssListTitleText"], "top", 5),
		(widgets["shotAssListTitleText"], "left", 65),
		(widgets["shotAssListCharText"], "top", 25),
		(widgets["shotAssListCharText"], "left", 5),
		(widgets["shotAssListPropText"], "top", 185),
		(widgets["shotAssListPropText"], "left", 5),
		(widgets["shotAssListSetText"], "top", 345),
		(widgets["shotAssListSetText"], "left", 5),
		])

				##############
				#shot List layout
				###############
	cmds.setParent(widgets["shotsFLO"])
	widgets["shotListCLO"] = cmds.columnLayout(w=130, bgc = (.5, .5, .5))
	widgets["shotListFLO"] = cmds.formLayout(w=130, h= 500)
	widgets["shotListTSL"] = cmds.textScrollList(w=130, h=430)
	widgets["shotListTitleText"] = cmds.text(l="Shot List", font = "boldLabelFont")
	widgets["shotListCharText"] = cmds.text(l="Shots")

	cmds.formLayout(widgets["shotListFLO"], e=True, af = [
		(widgets["shotListTSL"], "top", 40), 
		(widgets["shotListTSL"], "left", 0),
		(widgets["shotListTitleText"], "top", 5),
		(widgets["shotListTitleText"], "left", 30),
		(widgets["shotListCharText"], "top", 25),
		(widgets["shotListCharText"], "left", 5),
		])

				##############
				#shot Status layout
				###############	
	cmds.setParent(widgets["shotsFLO"])
	widgets["shotInfoAssListTLO"] = cmds.tabLayout(w=200, h=500)
	widgets["shotInfoFLO"] = cmds.formLayout("ShotInfo", w=200, h=500, bgc= (.5, .5, .5))
	widgets["shotInfoTitleText"] = cmds.text(l="Shot Information", font = "boldLabelFont")
	widgets["shotInfoNameText"] = cmds.text(l="<Shot Name>", font = "boldLabelFont")
	widgets["shotInfoPic"] = cmds.image(image = "H:/Windows/Desktop/kitten-photo-632-3.jpg", w= 154, h=154)
	widgets["shotAnmStatusTF"] = cmds.textFieldGrp(l="ANM STATUS: ", ed=False, cw = [(1, 70), (2, 100)])
	widgets["shotLgtStatusTF"] = cmds.textFieldGrp(l="LGT STATUS: ", ed=False, cw = [(1, 70), (2, 100)])
	widgets["shotFxStatusTF"] = cmds.textFieldGrp(l="FX STATUS: ", ed=False, cw = [(1, 70), (2, 100)])	
	cmds.formLayout(widgets["shotInfoFLO"], e=True, af =[
		(widgets["shotInfoNameText"], "top", 60),
		(widgets["shotInfoNameText"], "left", 10),
		(widgets["shotInfoPic"], "top", 100),
		(widgets["shotInfoPic"], "left", 23),
		(widgets["shotAnmStatusTF"], "top", 264),
		(widgets["shotAnmStatusTF"], "left", 10),
		(widgets["shotLgtStatusTF"], "top", 284),
		(widgets["shotLgtStatusTF"], "left", 10),
		(widgets["shotFxStatusTF"], "top", 304),
		(widgets["shotFxStatusTF"], "left", 10),		
		(widgets["shotInfoTitleText"], "top", 5),
		(widgets["shotInfoTitleText"], "left", 35),		
		])

	cmds.setParent(widgets["shotInfoAssListTLO"])
	widgets["shotAssRigListTLO"] = cmds.tabLayout("ProjRigs", w=200, h=500)	
	widgets["shotAssRigCharListCLO"] = cmds.columnLayout("Chars", w=200, h=500)
	widgets["shotAssRigCharListTSL"] = cmds.textScrollList(w=200, h=430)	
	cmds.setParent(widgets["shotAssRigListTLO"])
	widgets["shotAssRigPropListCLO"] = cmds.columnLayout("Props", w=200, h=500)
	widgets["shotAssRigPropListTSL"] = cmds.textScrollList(w=200, h=430)	
	cmds.setParent(widgets["shotAssRigListTLO"])
	widgets["shotAssRigSetListCLO"] = cmds.columnLayout("Sets", w=200, h=500)
	widgets["shotAssRigSetListTSL"] = cmds.textScrollList(w=200, h=430)	

				###############
				#Shot Action layout
				################
	cmds.setParent(widgets["shotsFLO"])
	widgets["shotActionFLO"] = cmds.formLayout(w=150, h=500, bgc =(.5, .5, .5))
	widgets["shotActionIconBut"] = cmds.button(l="Create shot Icon", w=130, h=20, bgc = (.7,.7,.7))
	widgets["shotActionRefAssBut"] = cmds.button(l="-> Ref Asset In ->", w=130, h=20, bgc = (.7,.7,.7))	
	widgets["shotActionImpBut"] = cmds.button(l="Import External", w=130, h=20, bgc = (.7,.7,.7))
	widgets["shotActionRefInBut"] = cmds.button(l="Reference External", w=130, h=20, bgc = (.7,.7,.7))
	widgets["shotActionDuplBut"] = cmds.button(l="Duplicate shot", w=130, h=20, bgc = (.7,.7,.7))
	widgets["shotActionReloadBut"] = cmds.button(l="Reload Reference ->", w=130, h=20, bgc = (.7,.7,.7))
	widgets["shotActionRemoveBut"] = cmds.button(l="Remove Reference ->", w=130, h=20, bgc = (.7,.7,.7))	
	widgets["shotActionArchBut"] = cmds.button(l="Archive shot", w=130, h=20, bgc = (.7,.7,.7))	
	widgets["shotActionTitle"] = cmds.text(l="Shot Actions", font = "boldLabelFont")
	widgets["shotActionCurText"] = cmds.text(l="Current Shot")
	widgets["shotActionCurTF"] = cmds.textField(w=150, en=False)

	cmds.formLayout(widgets["shotActionFLO"], e=True, af = [
		(widgets["shotActionTitle"], "top", 5),
		(widgets["shotActionTitle"], "left", 35),
		(widgets["shotActionCurText"], "top", 25),
		(widgets["shotActionCurText"], "left", 5),
		(widgets["shotActionCurTF"], "top", 45),
		(widgets["shotActionCurTF"], "left", 0),				
		(widgets["shotActionIconBut"], "top", 90),
		(widgets["shotActionIconBut"], "left", 10),
		(widgets["shotActionRefAssBut"], "top", 150),
		(widgets["shotActionRefAssBut"], "left", 10),
		(widgets["shotActionReloadBut"], "top", 180),
		(widgets["shotActionReloadBut"], "left", 10),
		(widgets["shotActionRemoveBut"], "top", 210),
		(widgets["shotActionRemoveBut"], "left", 10),						
		(widgets["shotActionImpBut"], "top", 310),
		(widgets["shotActionImpBut"], "left", 10),
		(widgets["shotActionRefInBut"], "top", 340),
		(widgets["shotActionRefInBut"], "left", 10),
		(widgets["shotActionDuplBut"], "top", 400),
		(widgets["shotActionDuplBut"], "left", 10),
		(widgets["shotActionArchBut"], "top", 430),
		(widgets["shotActionArchBut"], "left", 10),
		])

				###############
				#Shot anmLgt tab layout
				################
	cmds.setParent(widgets["shotsFLO"])
	widgets["anmLgtFLO"] = cmds.formLayout(w=250, h=500, bgc = (.4, .4, .4))
	widgets["anmLgtTLO"] = cmds.tabLayout(w=250, h=500, bgc = (.4,.4,.4))
					###############
					#shot anm tab layout
					###############
	widgets["anmTabCLO"] = cmds.columnLayout("ANM", w=250, bgc = (.5, .5, .5))
						#################
						#anm info frame and column layouts
						#################						
	cmds.separator(h=10, style="single")
	widgets["anmLastWSTFG"] = cmds.textFieldGrp(l="Latest WS: ", w=250, cw = [(1, 70), (2,160)], cal = [(1,"left"), (2, "left")],ed=False)
	widgets["anmLastMasterTFG"] = cmds.textFieldGrp(l="Master: ", w=250, cw = [(1, 70), (2,160)], cal = [(1,"left"), (2, "left")],ed=False)

	cmds.separator(h=20, style="single")
						#################
						#anm 'workshop' frame and column layouts
						#################
	cmds.setParent(widgets["anmTabCLO"])
	widgets["anmWSFLO"] = cmds.frameLayout("Anim Workshop", w=250, h=200, bgc= (.5, .5, .5), bs= "etchedIn")
	widgets["anmWSFoLO"] = cmds.formLayout(w=250, h=200, bgc = (.5,.5,.5))
	widgets["anmWSLogTitle"] = cmds.text(l=" Latest Log")
	widgets["anmWSLogTF"] = cmds.textField(w=250, ed=False)
	widgets["anmWSOpenBut"] = cmds.button(l="Open Latest Anim Workshop", w=200, bgc = (.4,.5,.8), ann=ann["openAnmWS"])
	widgets["anmWSIncrBut"] = cmds.button(l="Increment Anim Workshop", w=200, bgc = (.7,.6,.4), ann=ann["incrAnmWS"])
	widgets["anmWSPrevBut"] = cmds.button(l="Previous Anim Workshops", w=200, bgc = (.7,.7,.7), ann=ann["prevAnmWS"])
	cmds.formLayout(widgets["anmWSFoLO"], e=True, af = [
		(widgets["anmWSLogTitle"], "left", 0),
		(widgets["anmWSLogTitle"], "top", 5),
		(widgets["anmWSLogTF"], "left", 0),
		(widgets["anmWSLogTF"], "top", 20),
		(widgets["anmWSOpenBut"], "left", 25),
		(widgets["anmWSOpenBut"], "top", 50),
		(widgets["anmWSIncrBut"], "left", 25),
		(widgets["anmWSIncrBut"], "top", 80),
		(widgets["anmWSPrevBut"], "left", 25),
		(widgets["anmWSPrevBut"], "top", 150)		
		])
						#################
						#anm 'master' frame and column layouts
						#################
	cmds.setParent(widgets["anmTabCLO"])
	widgets["anmMstFLO"] = cmds.frameLayout("Anim Master", w=250, h=200, bgc= (.5, .5, .5), bs="etchedIn")
	widgets["anmMstFoLO"] = cmds.formLayout(w=250, h=200, bgc = (.5,.5,.5))
	widgets["anmMstLogTitle"] = cmds.text(l=" Latest Log")
	widgets["anmMstLogTF"] = cmds.textField(w=250, ed=False)
	widgets["anmMstOpenBut"] = cmds.button(l="Open Anim Master", w=200, bgc = (.5,.7,.5), ann=ann["openAnmMst"])
	widgets["anmMstIncrBut"] = cmds.button(l="Publish Anim Master", w=200, bgc = (.7,.5,.5), ann=ann["pubAnmMst"])
	widgets["anmMstPrevBut"] = cmds.button(l="Previous Anim Masters", w=200, bgc = (.3,.3,.3), ann=ann["prevAnmMst"])	
	cmds.formLayout(widgets["anmMstFoLO"], e=True, af = [
		(widgets["anmMstLogTitle"], "left", 0),
		(widgets["anmMstLogTitle"], "top", 5),
		(widgets["anmMstLogTF"], "left", 0),
		(widgets["anmMstLogTF"], "top", 20),
		(widgets["anmMstOpenBut"], "left", 25),
		(widgets["anmMstOpenBut"], "top", 50),
		(widgets["anmMstIncrBut"], "left", 25),
		(widgets["anmMstIncrBut"], "top", 80),
		(widgets["anmMstPrevBut"], "left", 25),
		(widgets["anmMstPrevBut"], "top", 150)			
		])
					###############
					#shot Lgt tab layout
					################	
	cmds.setParent(widgets["anmLgtTLO"])				
	widgets["lgtTabCLO"] = cmds.columnLayout("LGT", w=250, bgc = (.5,.5,.5))
						#################
						#lgt info frame and column layouts
						#################						
	cmds.separator(h=10, style="single")
	#widgets["lgtTitle"] = cmds.text(l = "lgt")
	#widgets["lgtLastWSTFG"] = cmds.textFieldGrp(l="Latest WS: ", w=250, cw = [(1, 70), (2,160)], cal = [(1,"left"), (2, "left")],ed=False)
	#widgets["lgtLastMasterTFG"] = cmds.textFieldGrp(l="Master: ", w=250, cw = [(1, 70), (2,160)], cal = [(1,"left"), (2, "left")],ed=False)
	widgets["lgtVariationsTSL"] = cmds.textScrollList(w=250, h=90)

	cmds.separator(h=10, style="single")
						#################
						#lgt 'workshop' frame and column layouts
						#################
	cmds.setParent(widgets["lgtTabCLO"])
	widgets["lgtWSFLO"] = cmds.frameLayout("Lighting Workshop", w=250, h=200, bgc= (.3, .3, .3), bs= "etchedIn")
	widgets["lgtWSFoLO"] = cmds.formLayout(w=250, h=200, bgc = (.5,.5,.5))
	widgets["lgtWSLogTitle"] = cmds.text(l=" Latest Log")
	widgets["lgtWSLogTF"] = cmds.textField(w=250, en=False)
	widgets["lgtWSOpenBut"] = cmds.button(l="Open Latest Light Workshop", w=200, bgc = (.4,.5,.8))
	widgets["lgtWSNewVarBut"] = cmds.button(l="Create New Variant WS", w=200, bgc = (.4,.4,.4))	
	widgets["lgtWSIncrBut"] = cmds.button(l="Increment Light Workshop", w=200, bgc = (.7,.6,.4))
	widgets["lgtWSPrevBut"] = cmds.button(l="Previous Light Workshops", w=200, bgc = (.7,.7,.7))	
	cmds.formLayout(widgets["lgtWSFoLO"], e=True, af = [
		(widgets["lgtWSLogTitle"], "left", 0),
		(widgets["lgtWSLogTitle"], "top", 5),
		(widgets["lgtWSLogTF"], "left", 0),
		(widgets["lgtWSLogTF"], "top", 20),
		(widgets["lgtWSNewVarBut"], "left", 25),
		(widgets["lgtWSNewVarBut"], "top", 110),		
		(widgets["lgtWSOpenBut"], "left", 25),
		(widgets["lgtWSOpenBut"], "top", 50),
		(widgets["lgtWSIncrBut"], "left", 25),
		(widgets["lgtWSIncrBut"], "top", 80),
		(widgets["lgtWSPrevBut"], "left", 25),
		(widgets["lgtWSPrevBut"], "top", 150)			
		])	
						#################
						#lgt 'master' frame and column layouts
						#################
	cmds.setParent(widgets["lgtTabCLO"])
	widgets["lgtMstFLO"] = cmds.frameLayout("Lighting Master", w=250, h=200, bgc= (.3, .3, .3), bs="etchedIn")
	widgets["lgtMstFoLO"] = cmds.formLayout(w=250, h=200, bgc = (.5,.5,.5))
	widgets["lgtMstLogTitle"] = cmds.text(l=" Latest Log")
	widgets["lgtMstLogTF"] = cmds.textField(w=250, en=False)
	widgets["lgtMstOpenBut"] = cmds.button(l="Open Light Master", w=200, bgc = (.5,.7,.5))
	widgets["lgtMstIncrBut"] = cmds.button(l="Publish Master", w=200, bgc = (.7,.5,.5))
	widgets["lgtMstPrevBut"] = cmds.button(l="Previous Light Masters", w=200, bgc = (.3,.3,.3))		
	cmds.formLayout(widgets["lgtMstFoLO"], e=True, af = [
		(widgets["lgtMstLogTitle"], "left", 0),
		(widgets["lgtMstLogTitle"], "top", 5),
		(widgets["lgtMstLogTF"], "left", 0),
		(widgets["lgtMstLogTF"], "top", 20),
		(widgets["lgtMstOpenBut"], "left", 25),
		(widgets["lgtMstOpenBut"], "top", 50),
		(widgets["lgtMstIncrBut"], "left", 25),
		(widgets["lgtMstIncrBut"], "top", 80),
		(widgets["lgtMstPrevBut"], "left", 25),
		(widgets["lgtMstPrevBut"], "top", 150)	
		])	

					###############
					#shot anm tab layout
					###############
	cmds.setParent(widgets["anmLgtTLO"])
	widgets["fxTabCLO"] = cmds.columnLayout("FX", w=250, bgc = (.5, .5, .5))
						#################
						#fx info frame and column layouts
						#################						
	cmds.separator(h=10, style="single")
	widgets["fxLastWSTFG"] = cmds.textFieldGrp(l="Latest WS: ", w=250, cw = [(1, 70), (2,160)], cal = [(1,"left"), (2, "left")],ed=False)
	widgets["fxLastMasterTFG"] = cmds.textFieldGrp(l="Master: ", w=250, cw = [(1, 70), (2,160)], cal = [(1,"left"), (2, "left")],ed=False)

	cmds.separator(h=20, style="single")
						#################
						#fx 'workshop' frame and column layouts
						#################
	cmds.setParent(widgets["fxTabCLO"])
	widgets["fxWSFLO"] = cmds.frameLayout("FX Workshop", w=250, h=200, bgc= (.5, .5, .5), bs= "etchedIn")
	widgets["fxWSFoLO"] = cmds.formLayout(w=250, h=200, bgc = (.5,.5,.5))
	widgets["fxWSLogTitle"] = cmds.text(l=" Latest Log")
	widgets["fxWSLogTF"] = cmds.textField(w=250, en=False)
	widgets["fxWSOpenBut"] = cmds.button(l="Open Latest FX Workshop", w=200, bgc = (.4,.5,.8))
	widgets["fxWSIncrBut"] = cmds.button(l="Increment FX Workshop", w=200, bgc = (.7,.6,.4))
	widgets["fxWSPrevBut"] = cmds.button(l="Previous FX Workshops", w=200, bgc = (.7,.7,.7))		
	cmds.formLayout(widgets["fxWSFoLO"], e=True, af = [
		(widgets["fxWSLogTitle"], "left", 0),
		(widgets["fxWSLogTitle"], "top", 5),
		(widgets["fxWSLogTF"], "left", 0),
		(widgets["fxWSLogTF"], "top", 20),
		(widgets["fxWSOpenBut"], "left", 25),
		(widgets["fxWSOpenBut"], "top", 50),
		(widgets["fxWSIncrBut"], "left", 25),
		(widgets["fxWSIncrBut"], "top", 80),
		(widgets["fxWSPrevBut"], "left", 25),
		(widgets["fxWSPrevBut"], "top", 150)		
		])
						#################
						#fx 'master' frame and column layouts
						#################
	cmds.setParent(widgets["fxTabCLO"])
	widgets["fxMstFLO"] = cmds.frameLayout("FX Master", w=250, h=200, bgc= (.5, .5, .5), bs="etchedIn")
	widgets["fxMstFoLO"] = cmds.formLayout(w=250, h=200, bgc = (.5,.5,.5))
	widgets["fxMstLogTitle"] = cmds.text(l=" Latest Log")
	widgets["fxMstLogTF"] = cmds.textField(w=250, en=False)
	widgets["fxMstOpenBut"] = cmds.button(l="Open Latest FX Master", w=200, bgc = (.5,.7,.5))
	widgets["fxMstIncrBut"] = cmds.button(l="Publish FX Master", w=200, bgc = (.7,.5,.5))
	widgets["fxMstPrevBut"] = cmds.button(l="Previous FX Masters", w=200, bgc = (.4,.4,.4))	
	cmds.formLayout(widgets["fxMstFoLO"], e=True, af = [
		(widgets["fxMstLogTitle"], "left", 0),
		(widgets["fxMstLogTitle"], "top", 5),
		(widgets["fxMstLogTF"], "left", 0),
		(widgets["fxMstLogTF"], "top", 20),
		(widgets["fxMstOpenBut"], "left", 25),
		(widgets["fxMstOpenBut"], "top", 50),
		(widgets["fxMstIncrBut"], "left", 25),
		(widgets["fxMstIncrBut"], "top", 80),
		(widgets["fxMstPrevBut"], "left", 25),
		(widgets["fxMstPrevBut"], "top", 150)		
		])


	cmds.setParent(widgets["anmLgtFLO"])
	widgets["anmLgtTitleText"] = cmds.text(l="Shot Files", font = "boldLabelFont")	

	cmds.formLayout(widgets["anmLgtFLO"], e=True, af = [(widgets["anmLgtTitleText"], "top", 5), (widgets["anmLgtTitleText"], "left", 135)])


			###################
			# - -- Shot Tab form setup
			##################
	cmds.formLayout(widgets["shotsFLO"], e=True, af = [
		(widgets["shotListCLO"], "left", 0),
		(widgets["shotListCLO"], "top", 0),
		(widgets["anmLgtFLO"], "left", 134),
		(widgets["anmLgtFLO"], "top", 0),	
		(widgets["shotInfoAssListTLO"], "left", 387),
		(widgets["shotInfoAssListTLO"], "top", 0),
		(widgets["shotActionFLO"], "top", 0),
		(widgets["shotActionFLO"], "left", 594),
		(widgets["shotAssListCLO"], "top", 0),
		(widgets["shotAssListCLO"], "left", 752)
		])


			################
			#Misc tab
			################
	cmds.setParent(widgets["lowTLO"])
	widgets["miscCLO"] = cmds.columnLayout("Other Pipeline Tools",w=1000, h=500, bgc = (.4,.4,.4))
	cmds.text(l="TODO - export cam(s) for nuke, etc")
	cmds.text(l="TODO - create a new char")	
	cmds.text(l="TODO - blasting, rendering stuff?")
	cmds.text(l="TODO - export data (text file of scene locations?)")
	cmds.text(l="TODO - convert an external image to icon (char or project)")
	cmds.text(l="TODO - revert ['ROLL BACK'] to master version? (replaces master and grabs that workshop")
	cmds.text(l="TODO - function to add your folder to the WIP folder in this project - save current to WIP folder")

	######################
	#show window
	######################
	cmds.window(widgets["win"], e=True, w=1000, h=580)
	cmds.showWindow(widgets["win"])

	#start us off
	populateWindow()


#######################################################################################################
# Functionality
#######################################################################################################

#############
# Get current Project
#############
def populateWindow(*args):
	#call out to chrlxFuncs to get current project
	current = cFuncs.getCurrentProject()
	project = ""
	job = ""
	updateSceneName()
	pi.openSceneFullPath = cFuncs.fixPath(cmds.file(q=True, sn=True))
	clearAll()

	openScene = os.path.basename(cmds.file(q=True, sn=True))
	if current:
		#check if this is valid charlex job
		try: 

###########------------fill these all in based on the project/job/spot

			projJob = current.rpartition("/jobs/")[2]
			#return project name - pass that to window
			project = projJob.partition("/")[0]
			job = projJob.partition("/")[2]
			
			#set some global variables to use later
			pi.currentProject = current
			pi.job = project
			pi.spot = job
			pi.openScene = openScene
			pi.charFolder = current + "/scenes/master/char"
			pi.propFolder = current + "/scenes/master/props"
			pi.setFolder = current + "/scenes/master/set"						
			pi.shotsFolder = current + "/scenes"
			pi.spotRefFolder = current + "/reference"
			cmds.text(widgets["projectText"], e=True, l=projJob)
			cmds.text(widgets["sceneText"], e=True, l=openScene)

		except:
			cmds.warning("There was some issue with the project. Perhaps its not a Charlex Job?")

		#get assets and populate list
		if project:
			populateShots(pi.currentProject)

	else: 
		cmds.warning("Doesn't seem like you're in project")

def exploreReference(*args):
	#just open the file browser to this folder
	if sys.platform == "win32":
		winPath = pi.spotRefFolder.replace("/", "\\")
		browser.open(winPath)
	elif sys.platform == "darwin":
		pass
	elif sys.platform == "linux" or sys.platform=="linux2":
		pass


def populateShots(current, *args):
	
	shotExclude = ["master", "prepro", "launchExample", ".mayaSwatches", ".directory"]
	
	cmds.textScrollList(widgets["shotListTSL"], e=True, ra=True)
########## - here also clear out the "assets in current scene"	

	shotList = cFuncs.getProjectShotList(current)
	if shotList:
		for shot in shotList:
			if shot not in shotExclude:
				cmds.textScrollList(widgets["shotListTSL"], e=True, a=shot, sc = updateShotInfo)

def updateShotInfo(shot = "", *args):
	"""updates the info in the geo/rig tab for the currently selected asset in the list"""

######---------reset the pi variables for the shot stuff	
	#if no shot passed in
	if not shot:
		try:
			shot = cmds.textScrollList(widgets["shotListTSL"], q=True, si=True)[0]

			pi.currentShot = shot
			#get some more info for stupid lighting naming
			pi.currentJobNumber = cFuncs.getJobNumber(pi.spot)
			pi.currentShotNum = cFuncs.getShotNumber(pi.currentShot)

			pi.currentShotFolder = "%s/%s"%(pi.shotsFolder, pi.currentShot)

			pi.currentAnmFolder = "%s/%s"%(pi.currentShotFolder, "anm")
			pi.currentLgtFolder = "%s/%s"%(pi.currentShotFolder, "lgt")
			pi.currentFxFolder = "%s/%s"%(pi.currentShotFolder, "fx")

		except:
			cmds.warning("chrlxshotWin.updateShotInfo: Couldn't acces the list info. Anything selected?")
	
	if shot:
		cmds.text(widgets["shotInfoNameText"], e=True, l=shot)

		#anm
		anmWS = cFuncs.getLatestAnmWS(pi.currentShot, pi.currentAnmFolder, "anm")

		if anmWS:
			cmds.textFieldGrp(widgets["shotAnmStatusTF"], e=True, tx = "WORKSHOPPED")
			cmds.textFieldGrp(widgets["anmLastWSTFG"], e=True, tx = os.path.basename(anmWS))
			pi.currentShotLatestAnmWS = anmWS
		else:
			cmds.textFieldGrp(widgets["shotAnmStatusTF"], e=True, tx = "-")
			cmds.textFieldGrp(widgets["anmLastWSTFG"], e=True, tx= "-")
			pi.currentShotLatestAnmWS = ""			

		anmMaster = cFuncs.getAnmMaster(shot, pi.currentAnmFolder)
		if anmMaster:
			cmds.textFieldGrp(widgets["shotAnmStatusTF"], e=True, tx = "MASTERED")
			cmds.textFieldGrp(widgets["anmLastMasterTFG"], e=True, tx = os.path.basename(anmMaster))
			pi.currentShotAnmMaster = anmMaster
		else:
			cmds.textFieldGrp(widgets["shotAnmStatusTF"], e=True, tx = "-")
			cmds.textFieldGrp(widgets["anmLastMasterTFG"], e=True, tx = "-")
			pi.currentShotAnmMaster = ""
############  here we'll have to parse our name
		#lgt
		# lgtWS = cFuncs.getLatestLgtWS(pi.currentJobNumber, pi.currentShotNum, pi.currentLgtFolder, "lgt")
		# if lgtWS:
		# 	cmds.textFieldGrp(widgets["shotLgtStatusTF"], e=True, tx = "WORKSHOPPED")
		# 	cmds.textFieldGrp(widgets["lgtLastWSTFG"], e=True, tx = os.path.basename(lgtWS))
		# 	pi.currentShotLatestLgtWS = lgtWS
		# else:
		# 	cmds.textFieldGrp(widgets["shotLgtStatusTF"], e=True, tx = "-")
		# 	cmds.textFieldGrp(widgets["lgtLastWSTFG"], e=True, tx= "-")
		# 	pi.currentShotLgtWS = ""

		# lgtMaster = cFuncs.getLgtMaster(pi.currentJobNumber, pi.currentShot, pi.currentLgtFolder)
		# if lgtMaster:
		# 	cmds.textFieldGrp(widgets["assetRigStatusTF"], e=True, tx = "MASTERED")
		# 	cmds.textFieldGrp(widgets["rigLastMasterTFG"], e=True, tx = os.path.basename(lgtMaster))
		# 	pi.currentAssetlgtMaster = lgtMaster
		# else:
		# 	cmds.textFieldGrp(widgets["shotLgtStatusTF"], e=True, tx = "-")
		# 	cmds.textFieldGrp(widgets["lgtLastMasterTFG"], e=True, tx = "-")
		# 	pi.currentShotLgtMaster = ""		

##########################----------DO ALL FOR FX

		#upate pic
		refDir = "%s/reference"%pi.currentShotFolder
		pic1 = "%sIcon.png"%shot
		pic2 = "%sIcon.xpm"%shot

		if os.path.isdir(refDir):
			if pic1 in (os.listdir(refDir)):
				cmds.image(widgets["shotInfoPic"], e=True, image = "%s/%s"%(refDir, pic1))
			elif pic2 in (os.listdir(refDir)):
				cmds.image(widgets["shotInfoPic"], e=True, image = "%s/%s"%(refDir, pic2))
			else:
				print"chrlxshotWin.updateShotInfo: Couldn't find the icon pic for: %s"%(refDir + "/" + shot)
			##### HERE get the default picture
		else:
			print "chrlxshotWin.updateShotInfo: Couldn't find the 'reference' directory for %s"%shot
	else:
		cmds.warning("chrlxshotWin.updateShotInfo: There is no shot name passed to me")		#get anm WS


############
# Set Project in Win
############	
def setProject(*args):
	projectSetter.projectSetter()

############
# Open Workshop and master files
############

def openAnmWS(*args):
	pass

def openAnmMaster(*args):
	pass

def openFile(*args):
	#go to the dir and open the file 
	#update the - Asset Info/Shot Info, Assets in Scene 
	pass

def updateSceneName(*args):
	"""gets the open scene name, updates the window text and the class variable"""
	openScene = os.path.basename(cmds.file(q=True, sn=True))
	cmds.text(widgets["sceneText"], e=True, l=openScene)
	pi.openScene= openScene

#############
# increment Workshops
#############

def incrementWorkshop(ftype, *args):
	#get info from window about what KIND of WS file it is (geo, rig, anm, lgt or fx)
	#call out to chrlxFuncs to increment file num	
	thisAsset = pi.currentAsset
	incr = ""

	if ftype == "geo":
		incr = cFuncs.incrementWS(pi.currentAssetGeoWS)
	elif ftype == "rig":
		incr = cFuncs.incrementWS(pi.currentAssetRigWS)
	else:
		pass
	

#confirm save if the file and the asset don't match = this can be a confirmDialog window, name buttonss based on files (the current file incr
#vs the attempted save increment). Use this info to name the saved file [basically I need to get the latest Ws and incr from the current files
#, NOT the one from the file win]

	pi.date = cmds.about(cd=True)
	pi.time = cmds.about(ct=True)

	#pull up prompt dialogue for notes
	note = cmds.promptDialog(t="Increment Workshop", m = os.path.basename(incr), sf = True, b = ("Add and Save", "Cancel"), db = "Add and Save", cb = "Cancel", ds = "Cancel")
	if note == "Add and Save":
		print "i'm adding the note: {0}".format(cmds.promptDialog(q=True, t = True))
		cmds.file(rename = incr)
		cmds.file(s=True, defaultExtensions=False, type="mayaAscii")
#confirmation dialogue that the scene has saved, THIS will refresh the window
#finish = cmds.confirmDialog(t= "Confirmation", m= "Scene Saved: \n{0}".format(os.path.basename(incr)))

		#updateAssetInfo(thisAsset)
		updateSceneName()
#populateWindow() or at least refresh the open scene

	else:
		pass


#############
# create icon script
############

# def createAssetIcon(*args):
# 	#call to external to create icons
# 	#check if user is in the same scene file as the selected asset!!
# 	sname = cFuncs.fixPath(cmds.file(q=True, sn = True))
# 	snameChar = os.path.commonprefix([sname, pi.currentAssetFolder])
# 	print "the common prefix is ", snameChar

# 	sceneCont = "Yes"
# 	if snameChar != pi.currentAssetFolder:
# 		sceneCont = cmds.confirmDialog(t="Mismatching Chars", m="Your scene doesn't match that asset!\nWrite icon to %s anyways?"%pi.currentAsset, b=("Yes","No"), db="No", cb="No", ds="No")
# ##### HERE above ==== > create a confirm dialog with the actual names of the assets/folders
# 	#check that something is selected in asset list
# 	if sceneCont == "Yes":
# 		sel = ""
# 		try:
# 			sel = cmds.textScrollList(widgets["assCharListTSL"], q=True, si=True)[0]
# 		except: 
# 			cmds.warning("Doesn't seem like you've selected an asset to create an image for!")

# 		if sel:
# 			go = "Yes"
# 			#CHECK IF THERES ALREADY AN IMAGE
# 			iconFile = "%s/reference/%sIcon.png"%(pi.currentAssetFolder, pi.currentAsset)
# 			if os.path.isfile(iconFile):
# 				go = cmds.confirmDialog(t="Overwrite Confirm", m="There is already an icon for this!\nShould I overwrite it?", b=("Yes", "No"), db="Yes", cb ="No", ds = "No")
# 			if go=="Yes":
# 				#at this pt we can delete the orig file
# 				if os.path.isfile(iconFile):
# 					os.remove(iconFile)
# 				#deselect objects in scene, PB, then reselect
# 				sl = cmds.ls(sl=True)
# 				cmds.select(clear = True)
# 				cFuncs.createAssetIcon("%s/reference"%pi.currentAssetFolder, pi.currentAsset)
# 				cmds.select(sl, r=True)

# 				updateAssetInfo(pi.currentAsset)
# 			else:
# 				cmds.warning("Icon creation cancelled")
# 	else:
# 		cmds.warning("Cancelling Icon Creation")

def clearAll(*args):
	cmds.textScrollList(widgets["shotAssRigCharListTSL"], e=True, ra =True)
	cmds.textScrollList(widgets["shotAssRigPropListTSL"], e=True, ra =True)
	cmds.textScrollList(widgets["shotAssRigSetListTSL"], e=True, ra =True)	

	cmds.textScrollList(widgets["shotListTSL"], e=True, ra=True)	

	#anm
	cmds.textField(widgets["anmWSLogTF"], e=True, tx= "")
	cmds.textField(widgets["anmMstLogTF"], e=True, tx="")	
	cmds.textFieldGrp(widgets["anmLastWSTFG"], e=True, tx = "")
	cmds.textFieldGrp(widgets["anmLastMasterTFG"], e=True, tx="")

	#lgt
	cmds.textScrollList(widgets["lgtVariationsTSL"], e=True, ra= True)

	#shot info
	cmds.image(widgets["shotInfoPic"], e=True, image = "H:/Windows/Desktop/kitten-photo-632-3.jpg")
	cmds.textFieldGrp(widgets["shotAnmStatusTF"], e=True, tx="")
	cmds.textFieldGrp(widgets["shotLgtStatusTF"], e=True,tx="")
	cmds.textFieldGrp(widgets["shotFxStatusTF"], e=True, tx="")	
	#projectJob
	#currentScene

#############
# Call to start UI
############

def shotWin(*args):
	shotWinUI()

