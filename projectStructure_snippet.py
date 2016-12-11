class Project(object):

	def __init__(self):
		##############----needs specific
		#job
		self.job = "JOBNAME_P#####"

		##############----needs specific		#spot
		self.spot = "{0}/SPOTNAME".format(self.job)


		#each spot
		self.assets = "{0}/assets".format(self.spot)
		self.sandbox = "{0}/sandbox".format(self.spot)
		self.shots = "{0}/shots".format(self.spot)
		self.workspace = "{0}/workspace.mel".format(self.spot)
		self.config = "{0}/z_config".format(self.spot)
		self.projData = "{0}/z_maya_project".format(self.spot)

		#renders
		self.renders = "{0}/renders".format(self.spot)

		###############
		# ASSETS
		###############

		#assets
		self.characters = "{0}/characters".format(self.assets)
		self.sets = "{0}/sets".format(self.assets)
		self.props = "{0}/props".format(self.assets)
		self.sourceImages = "{0}/sourceImages".format(self.assets)
		self.shaders = "{0}/shaders".format(self.assets)
		self.mtl = "{0}/mtl".format(self.assets)
		self.lightRigs = "{0}/lightRigs".format(self.assets)
		self.layouts = "{0}/layouts".format(self.assets)

		#houdini folder
		self.shotsHoudini = "{0}/shots".format(self.shots)
		
		##############----needs specific (need assetName, assetType)
		#characters/set/props/layouts
		self.character = "{0}/CHARACTERNAME".format(self.characters)
		self.prop = "{0}/PROPNAME".format(self.props)
		self.set = "{0}/SETNAME".format(self.props)
		self.layout = "{0}/LAYOUTNAME".format(self.props)

		#asset component setup
		self.geo = "{0}/geo".format(self.character)
		self.geoWS = "{0}/workshops".format(self.geo)
		self.geoVersions = "{0}/past_versions".format(self.geo)
		self.impExp = "{0}/import_export".format(self.geo)
		
		self.rig = "{0}/rig".format(self.character)
		self.rigWS = "{0}/workshops".format(self.rig)
		self.rigVersions = "{0}/pastVersions".format(self.rig)
		
		self.reference = "{0}/reference".format(self.character)
		self.sourceImages = "{0}/sourceImages".format(self.character)


		############
		# SHOTS
		############

		###########----needs specific (needs shotName, shotType, variantName)
		#shot/dev/previz shot folder
		self.shot = "{0}/SHOTNAME".format(self.shots)

		#############----------this should be inside the specific shot folder
		self.anm = "{0}/anm".format(self.shot)
		self.anmShot = "{0}/ANMVAR"
		self.anmWS = "{0}/workshops".format(self.anmShot)
		self.anmVersions = "{0}/past_versions".format(self.anmShot)
		#anm master live here

		self.lgt = "{0}/lgt".format(self.shot)
		self.lgtShot = "{0}/LGTVAR".format(self.lgt)
		self.lgtWS = "{0}/workshops".format(self.lgtShot)
		self.lgtVersions = "{0}/past_versions".format(self.lgtShot)
		#lgt master lives here

		######## needs FXVAR
		self.fx = "{0}/fx".format(self.shot)
		self.fxShot = "{0}/FXVAR".format(self.fx)
		self.fxWS = "{0}/workshops".format(self.fxShot)
		self.fxVersions = "{0}/past_versions".format(self.fxShot)

		self.data = "{0}/data".format(self.shot)
		# abc, ass, fbx, obj, cam, vdb, anm

		#render dirs, needs shotName
		self.shotRender = "{0}/SHOTNAME".format(self.renders)
		self.anmFrames = "{0}/anm_frames".format(self.renders)
		self.fxFrames = "{0}/fx_frames".format(self.renders)
		self.renderFrames = "{0}/render_frames/maya".format(self.renders)
		self.wipFrames = "{0}/wip_frames".format(self.renders)