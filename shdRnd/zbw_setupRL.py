import maya.cmds as cmds
from functools import partial
import maya.mel as mel

widgets = {}
renderLayer = {"CarKey":"Car_Key", "CarEnv":"Car_Env", "BGKey":"BG_Key", "BGEnv":"BG_Env", "AO":"ALL_AO", "MatteA":"ALL_MatteA", "MatteB":"ALL_MatteB", "MoVec":"ALL_MoVec", "Shadow":"ALL_Shadow"}

#UI
def setupRLUI():
    if cmds.window("RLWin", exists=True):
        cmds.deleteUI("RLWin")
    
    widgets["win"] = cmds.window("RLWin", t="zbw_setupRL", w=200, h=400)
    widgets["mainCL"] = cmds.columnLayout(w=200)
    widgets["mainFrame"] = cmds.frameLayout(l="Create Render Layers", w=200, cll=True, bgc=(.2,.2,.2))
    
    widgets["CarKey"] = cmds.checkBox(l="Car_Env", v=True)
    widgets["CarEnv"] = cmds.checkBox(l="Car_Key", v=True)
    widgets["BGKey"] = cmds.checkBox(l="BG_Env", v=True)
    widgets["BGEnv"] = cmds.checkBox(l="BG_Key", v=True)
    widgets["AO"] = cmds.checkBox(l="All_AO", v=True)
    widgets["MatteA"] = cmds.checkBox(l="All_MatteA", v=True)
    widgets["MatteB"] = cmds.checkBox(l="All_MatteB", v=True)
    widgets["MoVec"] = cmds.checkBox(l="All_MoVec", v=True)
    widgets["Shadow"] = cmds.checkBox(l="All_Shadow", v=True)
    
    widgets["createBut"] = cmds.button(l="Create Layers", w=200, h=40, bgc=(.6,.8,.6), c=createRL)
    cmds.text("NOTE: this is setting the overrides for \nthe moVec layer RG's and materials \n(if you have them in scene\n for the AO and Movec layers but \n NO passes are set up")
    cmds.separator(h=20, style = "double")
    #widgets["copyBut"] = cmds.button(l="Copy Selected Layer", w=200, h=40, bgc=(.8,.8,.6), c=copyRL)
    #cmds.separator(h=20, style = "double")
    widgets["importBut"] = cmds.button(l="Import RL Shaders File", w=200, h=40, bgc=(.8,.6,.6), c=importRL)
   
    cmds.showWindow(widgets["win"])
    cmds.window(widgets["win"], e=True, w=200, h=400)
        
  
  
  
#create render layers
def createRL(*args):
    layers = []
    rls = ["CarKey", "CarEnv", "BGKey", "BGEnv", "AO", "MatteA", "MatteB", "MoVec", "Shadow"]
    
    movecShd = cmds.ls("*:*moVec_SHD")
    if not movecShd:
        movecShd = cmds.ls("*moVec_SHD")
    if movecShd:
        mvsg = cmds.listConnections(movecShd, type="shadingEngine")[0]
    else: 
        cmds.warning("Can't find the movec shader")
        
    aoShd = cmds.ls("*:*AO_SHD")
    if not aoShd:
        aoShd = cmds.ls("*AO_SHD")
    if aoShd:
        aosg = cmds.listConnections(aoShd, type="shadingEngine")[0]
    else:
        cmds.warning("can't find the ao shader")
        
    for rl in rls:
        if cmds.checkBox(widgets[rl], q=True, v=True):
            layers.append(rl)
    
    for each in layers:
        cmds.createRenderLayer(n=renderLayer[each], mc=True, empty=True)
        if each == "MoVec":
            cmds.editRenderLayerAdjustment('defaultArnoldRenderOptions.motion_blur_enable', lyr="ALL_MoVec")
            cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 1)
            cmds.editRenderLayerAdjustment("defaultArnoldRenderOptions.referenceTime", lyr="ALL_MoVec")
            cmds.setAttr("defaultArnoldRenderOptions.referenceTime", 0.5)
            cmds.editRenderLayerAdjustment("defaultArnoldRenderOptions.ignoreMotionBlur", lyr="ALL_MoVec")
            cmds.setAttr("defaultArnoldRenderOptions.ignoreMotionBlur", 1)
            print mvsg
            if mvsg:
                cmds.connectAttr("%s.message"%mvsg, "ALL_MoVec.shadingGroupOverride", f=True)

            
        if each == "AO":
            print aosg
            if aosg:
                cmds.connectAttr("%s.message"%aosg, "ALL_AO.shadingGroupOverride", f=True)
                
def copyRL(*args):
    pass
    
    
def importRL(*args):
    #import the file
    try:
        cmds.file("K:\NBC_Formula_1_011413\Production\Assets\Materials\matteAOMoVec_SHD.ma", i=True)
    except:
        cmds.warning("Can't find that the file")
    
def setupRL():	
    setupRLUI()