# dictionaries of tools registered for zTools 
# used to call from zTools using zTools.zAction, zTools.zMelAction
# value = [module, function] for python, [procedure] for mel

zRigDict = {
    "attr": ["zTools.rig.zbw_attributes", "attributes"],
    "snap": ["zTools.rig.zbw_snap", "snap"],
    "shpScl": ["zTools.rig.zbw_shapeScale", "shapeScale"],
    "selBuf": ["zTools.rig.zbw_selectionBuffer", "selectionBuffer"],
    "smIK": ["zTools.rig.zbw_smallIKStretch", "smallIKStretch"],
    "foll": ["zTools.rig.zbw_makeFollicle", "makeFollicle"],
    "ribbon": ["zTools.rig.zbw_ribbon", "ribbon"],
    "softMod": ["zTools.rig.zbw_softDeformer", "softDeformer"],
    "jntRadius": ["zTools.rig.zbw_jointRadius", "jointRadius"],
    "cmtRename": ["cometRename"],
    "trfmBuffer": ["zTools.rig.zbw_transformBuffer", "transformBuffer"],
    "crvTools": ["zTools.rig.zbw_curveTools", "curveTools"],
    "abSym": ['abSymMesh'],
    "cmtJntOrnt": ["cometJointOrient"],
    "autoSquash": ["zTools.rig.zbw_autoSquashRig", "autoSquashRig"],
    "BSpirit": ["BSpiritCorrectiveShape"],
    "follow": ["zTools.rig.zbw_followConstraints", "followConstraints"],
    "splineIK": ["zTools.rig.zbw_splineRig", "splineRig"],
    "leg": ["zTools.rig.zbw_rigger_legRig",  "LegRigUI"],
    "arm": ["zTools.rig.zbw_rigger_armRig", "ArmRigUI"],
    "typFind": ["zTools.rig.zbw_typeFinder", "typeFinder"],
    "wire": ["zTools.rig.zbw_wireRig", "wireRig"],
    "sphereCrvRig": ["zTools.rig.zbw_sphereCrvRig", "sphereCrvRig"],
    "softJoint": ["zTools.rig.zbw_softSelectionToJoint", "softSelectionToJoint"],
    "ikSpine":["zTools.rig.zbw_ikSpine", "ikSpine"],
}

zAnimDict = {
    "tween": ["zTools.anim.tweenMachine", "start"],
    "noise": ["zTools.anim.zbw_animNoise", "animNoise"],
    "audio": ["zTools.anim.zbw_audioManager", "audioManager"],
    "clean": ["zTools.anim.zbw_cleanKeys", "cleanKeys"],
    "dupe": ["zTools.anim.zbw_dupeSwap", "dupeSwap"],
    "huddle": ["zTools.anim.zbw_huddle", "huddle"],
    "randomSel": ["zTools.anim.zbw_randomSelection","randomSelection"],
    "randomAttr": ["zTools.anim.zbw_randomAttrs", "randomAttrs"],
    "clip": ["zTools.anim.zbw_setClipPlanes", "setClipPlanes"],
    "tangents": ["zTools.anim.zbw_tangents", "tangents"],
    "studioLib": ["studiolibrary", "main"], 
    "animBot": ["animBot", "welcome"], 
}

zModelDict = {
    "extend": ["zTools.model.zbw_polyExtend","polyExtend"],
    "wrinkle": ["zTools.model.zbw_wrinklePoly", "wrinklePoly"]
}

zShdDict = {
    "shdTransfer": ["zTools.shaderRender.zbw_shadingTransfer", "shadingTransfer"],
    "prvsShd": ["zTools.shaderRender.zbw_previsShaders", "previsShaders"],
    "shdSave": ["zTools.shaderRender.zbw_shaderSaver", "shaderSaver"],
}
