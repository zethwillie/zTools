# dictionaries of tools registered for zTools 
# key = what to call from dict
# value = code to run the tool

zRigDict = {
    "attr": "import zTools.rig.zbw_attributes as zat; reload(zat); zat.attributes()",
    "snap": "import zTools.rig.zbw_snap as snap; reload(snap), snap.snap()",
    "shpScl": "import zTools.rig.zbw_shapeScale as zss; zss.shapeScale()",
    "selBuf": "import zTools.rig.zbw_selectionBuffer as buf; reload(buf); buf.selectionBuffer()",
    "smIK": "import zTools.rig.zbw_smallIKStretch as zsik; zsik.smallIKStretch()",
    "foll": "import zTools.rig.zbw_makeFollicle as zmf; reload(zmf); zmf.makeFollicle()",
    "ribbon": "import zTools.rig.zbw_ribbon as zrib; reload(zrib); zrib.ribbon()",
    "soft": "import zTools.rig.zbw_softDeformer as zsft; reload(zsft); zsft.softDeformer()",
    "jntRadius": "import zTools.rig.zbw_jointRadius as jntR; jntR.jointRadius()",
    "cmtRename": "mel.eval('cometRename')",
    "trfmBuffer": "import zTools.rig.zbw_transformBuffer as ztbuf; reload(ztbuf); ztbuf.transformBuffer()",
    "crvTools": "import zTools.rig.zbw_curveTools as ctool; reload(ctool); ctool.curveTools()",
    "abSym": "mel.eval('abSymMesh')",
    "cmtJntOrnt": "mel.eval('cometJointOrient')",
    "autoSquash": "import zTools.rig.zbw_autoSquashRig as zAS; reload(zAS); zAS.autoSquashRig()",
    "BSpirit": "mel.eval('BSpiritCorrectiveShape')",
    "follow": "import zTools.rig.zbw_followConstraints as zFC; reload(zFC); zFC.followConstraints()",
    "splineIK": "import zTools.rig.zbw_splineRig as zspik; reload(zspik); zspik.splineRig()",
    "leg": "import zTools.rig.zbw_rigger_legRig as leg; reload(leg); LEG=leg.LegRigUI()",
    "arm": "import zTools.rig.zbw_rigger_armRig as arm; reload(arm); ARM = arm.ArmRigUI()",
    "typFind": "import zTools.rig.zbw_typeFinder as zType; reload(zType); zType.typeFinder()",
    "wire": "import zTools.rig.zbw_wireRig as wire; reload(wire); wire.wireRig()",
    "sphereCrvRig":"import zTools.rig.zbw_sphereCrvRig as zscr; reload(zscr); zscr.sphereCrvRig()",
}

zAnimDict = {
    "tween": "import zTools.anim.tweenMachine as tm; tm.start()",
    "noise": "import zTools.anim.zbw_animNoise as zAN; reload(zAN); zAN.animNoise()",
    "audio": "import zTools.anim.zbw_audioManager as zAM; reload(zAM); zAM.audioManager()",
    "clean": "import zTools.anim.zbw_cleanKeys as zCK; reload(zCK); zCK.cleanKeys()",
    "dupe": "import zTools.anim.zbw_dupeSwap as zDS; reload(zDS);zDS.dupeSwap()",
    "huddle": "import zTools.anim.zbw_huddle as zH; reload(zH);zH.huddle()",
    "randomSel": "import zTools.anim.zbw_randomSelection as zRS; reload(zRS);zRS.randomSelection()",
    "randomAttr": "import zTools.anim.zbw_randomAttrs as zRA; reload(zRA); zRA.randomAttrs()",
    "clip": "import zTools.anim.zbw_setClipPlanes as zSC; reload(zSC); zSC.setClipPlanes()",
    "tangents": "import zTools.anim.zbw_tangents as zTan; reload(zTan); zTan.tangents()",
    "studioLib": "import studiolibrary; studiolibrary.main()", 
    "animBot": "import animBot; animBot.welcome()", 
}

zModelDict = {
    "extend": "import zTools.model.zbw_polyExtend as zPE; reload(zPE); zPE.polyExtend()",
    "wrinkle": "import zTools.model.zbw_wrinklePoly as zWP; reload(zWP); zWP.wrinklePoly()"
}

zShdDict = {
    "shdTransfer": "import zTools.shaderRender.zbw_shadingTransfer as zST; reload(zST); zST.shadingTransfer()",
    "prvsShd": "import zTools.shaderRender.zbw_previsShaders as zPrvsShd; reload(zPrvsShd); zPrvsShd.previsShaders()",
    "shdSave": "import zTools.shaderRender.zbw_shaderSaver as zshSv; reload(zshSv); zshSv.shaderSaver()",
}
