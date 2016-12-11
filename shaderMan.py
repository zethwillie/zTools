'''
A tool for exporting, importing, and transferring shaders, layers, and render elements from one Maya file to others.
A "Repair" mode is also included, to help with fixing files for which changes in referenced files has caused broken shader assignments.
'''
__author__ = 'Salar Saleh'



import re
import logging
import sys
import glob
import os
import subprocess
import string
import shutil
from tempfile import mkstemp

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR) # For more verbosity, change ERROR to DEBUG.
import ConfigParser

import maya.cmds as cmds
import maya.mel as mel

import chrlx.utils as utils
import chrlx.maya.render.util
import chrlx.maya.scene.nodes as nds
import chrlx_scripts.filer

class ShaderManUI(object):
	def __init__(self):

		# test for batch mode
		batchMode = cmds.about(batch=1)

		# set import mode default
		importMode=1

		# are we in the backlot?
		backlot = 0
		importModeDefault = 1
		if ( os.path.split(cmds.workspace(q=True, fn=True))[1] == 'backlot' ):
			backlot = 1
			importModeDefault = 3

		# glob shader files
		shaderFileNames = []
		shaderFileBaseNames = self.listShaderFiles(importMode=1)[1]

		if ( batchMode == 0 ):
			# setup UI
			self.name = 'ShaderManUI'
			self.title = 'Shader Manager v3.4 (2014)'
			if (cmds.window(self.name, q=1, exists=1)):
				cmds.deleteUI(self.name)
			self.window = cmds.window(self.name, title=self.title)

			 # create UI
			form = cmds.formLayout()
			self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, changeCommand=self.refreshFileBaseList)
			cmds.formLayout( form, edit=True, attachForm=((self.tabs, 'top', 0), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)) )

			# export tab
			self.exportTab = cmds.rowColumnLayout(numberOfColumns=1)
			self.exportMode = cmds.radioButtonGrp( label='Export Mode:', labelArray2=['To MTL Files (Auto-Export)', 'To Custom Files'],\
				numberOfRadioButtons=2, vertical=True, select=1, onCommand=self.toggleFileBase )
			self.exportFileBase = cmds.textFieldGrp(label='Export File Base Name:', width=200, text='filename', enable=0)
			self.exportButton = cmds.button( label='Export Shaders', command=self.exportShaders )
			cmds.separator( width=428 )
			cmds.setParent( '..' )

			# import tab
			self.importTab = cmds.rowColumnLayout(numberOfColumns=1)
			self.importMode = cmds.radioButtonGrp( label='Import Mode:', labelArray3=['From MTL Files (Auto-Import All)', 'From MTL Files (Select Character/Layers)', 'From Custom Files'],\
				numberOfRadioButtons=3, vertical=True, select=importModeDefault, enable1=(1-backlot), enable2=(1-backlot), onCommand=self.toggleImportMode )
			self.importRenderSettings = cmds.checkBoxGrp( label='', label1='Import Render Settings', value1=0, numberOfCheckBoxes=1, changeCommand=self.renderSettingsCheckBoxChange, \
				annotation='Import Render Settings from ShaderMan files.')

			cmds.separator()
			self.selectedOnly = cmds.checkBoxGrp( label='', label1='Import Selected Objects Only', numberOfCheckBoxes=1, annotation='Import shaders only for the selected objects and their children.' )
			self.postDeleteUnused = cmds.checkBoxGrp( label='', label1='Delete Unused Shaders After Import', numberOfCheckBoxes=1, annotation='Delete unused shaders after running Import Shaders.' )
			self.looseMatchMode = cmds.checkBoxGrp( label='', label1='"Loose" Name Matching', numberOfCheckBoxes=1, \
				annotation='More lenient name matching, to help circumvent problems with non-standard object names.\nThis is only recommended if the default (Loose Name Matching OFF) is skipping over lots of objects.' )
			self.literalMode = cmds.checkBoxGrp( label='', label1='Literal Mode', numberOfCheckBoxes=1, \
				annotation='This will attach shaders to objects with the EXACT same names as the file they were exported from.  Useful for copying shader assignments from one file to another, rather than setting up lighting files from scratch.' )

			cmds.separator()
			self.replaceCharName = cmds.checkBoxGrp( label='', label1='Replace Character Name', value1=0, numberOfCheckBoxes=1, changeCommand=self.toggleReplaceCharName, \
				annotation='Replace a character name in the import file with another name in your scene.')
			self.charNameToReplace = cmds.textFieldGrp(label='Char Name to Replace:', width=200, text='from name', enable=0)
			self.charNameReplace = cmds.textFieldGrp(label='Char Name Replacement:', width=200, text='to name', enable=0)

			cmds.separator()
			self.filesText = cmds.text( label='Characters:', align='left', enable=0 )
			self.fileScrollList = cmds.textScrollList( numberOfRows=12, allowMultiSelection=False, append=shaderFileBaseNames, selectCommand=self.refreshLayerList, enable=0 )
			self.layersText = cmds.text( label='Layers:', align='left', enable=0 )
			self.layerScrollList = cmds.textScrollList( numberOfRows=12, allowMultiSelection=True, enable=0 )

			self.layerMode = cmds.radioButtonGrp( label='Import Layer Mode:', labelArray3=['New', 'Current', 'Merge'], enable2=0, numberOfRadioButtons=3, select=3 )
			self.refreshButton = cmds.button( label='Refresh List', command=self.refreshFileBaseList )
			self.importButton = cmds.button( label='Import Shaders', command=self.importShaders )
			cmds.separator( width=428 )
			cmds.setParent( '..' )

			# auto export all tab
			self.autoExportAllTab = cmds.rowColumnLayout(numberOfColumns=1)
			self.exportAllInfoText = cmds.text( label='\nThis button will export  ALL shader files for  ALL characters in the current job.\nThis option is disabled for the BACKLOT.\n', align='center' )
			self.autoExportAllButton = cmds.button( label='Export  ALL Characters in Current Job', enable=(1-backlot), command=self.autoExportAll )
			cmds.separator( width=428 )
			cmds.setParent( '..' )

			# repair tab
			self.repairTab = cmds.rowColumnLayout(numberOfColumns=1)
			self.repairInfoText = cmds.text( label='\nThis button will attempt to repair a lighting file for which shader assignments have become badly broken.\n\nThis will present you with the list of previous versions of anim, then recover whatever can be salvaged from your scene, and re-setup your file using the current anim master.\n', align='center', wordWrap=True, width=428 )
			cmds.separator( width=428 )
			self.repairInfoText4 = cmds.text( label='\n    Instructions:\n     1) Open the last lighting workshop from before the breakage.\n     2) Press the "Repair File..." button\n     3) Double-click the last anim file that was mastered before the breakage.\n     4) Wait a few seconds, then weep tears of joy.\n', align='left' )
			self.repairButton = cmds.button( label='Repair File...', enable=(1-backlot), command=self.repairFile)
			cmds.text( label='\n', align='left' )
			cmds.frameLayout( cll=1, cl=1, label='More Info', borderStyle='in' )
			self.repairInfoText2 = cmds.text( label='\n    What can be salvaged:\n     -Shader assignments (only for characters)\n     -Lights and per-layer light assignments\n     -Render layers and per-layer object assignments\n     -Render elements\n     -Render settings (for each layer)\n     -Display layers (but NOT display layer object assignments)', align='left' )
			self.repairInfoText3 = cmds.text( label='\n    What can NOT be salvaged:\n     -Face assignments\n     -Object render stats\n     -3D Texture nodes will be imported, but will not be parented to characters\n', align='left' )
			cmds.setParent( '..' )
			cmds.setParent( '..' )

			'''
			# prefs tab
			self.prefsTab = cmds.rowColumnLayout(numberOfColumns=1)
			self.prefsInfoText = cmds.text( label='\nThis tab is for managing ShaderMan prefs.\nThese prefs are shared by all characters and shots within your current SPOT.\n', align='center' )
			self.prefsFilesText = cmds.text( label='Render Settings Character:', align='left', enable=1 )
			self.prefsFileScrollList = cmds.textScrollList( numberOfRows=12, allowMultiSelection=False, append=shaderFileBaseNames, selectCommand=self.refreshLayerList, enable=1, si=self.renderSettingsChar )
			self.savePrefsButton = cmds.button( label='Set Render Settings Character', enable=(1-backlot), command=self.savePrefs)
			cmds.separator( width=428 )
			cmds.setParent( '..' )
			'''

			# tab layout
			cmds.tabLayout( self.tabs, edit=True, tabLabel=((self.exportTab, 'Export'), (self.importTab, 'Import'), (self.autoExportAllTab, 'Multi-Char Exporter'), (self.repairTab, 'Repair')))
			cmds.window(self.name, e=1, w=435, h=728, sizeable=0)
			cmds.showWindow()


	def exportShaders(self, exportMode = 1, *args):
		'''
		exportFileBase = base name to insert in the exported file name
		export modes:
		  0: Custom Files mode (radio button #2)
		  1: Character MTL mode (radio button #1)
		  2: AutoBackup mode (no radio button value)
		'''
		renderLayers = []
		shapeListClean =[]
		renderLayersClean = []
		shaderObjects = ''
		chars = ''
		charList = []
		layerMembers = []
		shader = ''
		exportFileBase = ''

		# test for batch mode
		batchMode = cmds.about(batch=1)

		# read the state of the UI buttons, if interactive mode
		log.debug('exportMode: %s' % exportMode)
		if (batchMode == 0):
			if (exportMode == 2):
				log.debug('EXPORT MODE 2\n')
			else:
				exportModeButton = cmds.radioButtonGrp(self.exportMode, q=True, select=True)
				if (exportModeButton == 2):
					exportMode = 0
				else:
					exportMode = exportModeButton
				exportFileBase = cmds.textFieldGrp(self.exportFileBase, query=True, text=True)
		log.debug('exportMode now: %s' % exportMode)

		# build the list of render layers
		renderLayers = cmds.ls(type='renderLayer')
		for renderLayer in renderLayers:
			if (cmds.getAttr(renderLayer + '.renderable') == False):
				continue
			if (re.match(r".*defaultRenderLayer.*", renderLayer)):
				if renderLayer != 'defaultRenderLayer':
					print ('Warning: This file has a renderLayer called: %s' % renderLayer)
				continue
			renderLayersClean = renderLayersClean + [renderLayer]
		log.debug("renderLayer list is %s: " % renderLayersClean)
		if (renderLayersClean == []):
			cmds.confirmDialog( title='Alert', messageAlign='center', message=\
				'No active render layers were found in the file. Doing nothing.'\
				, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
			sys.exit()
		
		# build the list of objects to export
		# Character MTL mode
		if (exportMode == 1):
			# pull char name from maya file name
			autoCharName = self.parseFileName() 
			log.debug("From MTL mode char list is %s: " % autoCharName)
			if (autoCharName == None):
				cmds.confirmDialog( title='Alert', messageAlign='center', message=\
				'Character name could not be determined from maya file name.  Please make sure you are in an \"mtl\" file.'
				, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
				sys.exit()
			# parse the reference
			try:
				shapeList = cmds.referenceQuery( 'geoRN',nodes=True )
			except:
				try:
					shapeList = cmds.referenceQuery( (autoCharName + 'RN'),nodes=True )
				except:
					cmds.confirmDialog( title='Alert', messageAlign='center', message=\
						'ERROR: No geo file reference found.\n\nMake sure this file is referencing your geo file, and that the reference prefix is "geo". Doing nothing.'\
						, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
					sys.exit()
			cmds.select(shapeList,replace=True)
			shapeListClean = self.getShapeList()
		# Shot-to-shot mode
		elif (exportMode == 0):
			shapeListClean = self.getShapeList()
		# AutoBackup mode
		elif (exportMode == 2):
			print('AUTO BACKUP MODE')
			cmds.select('*GOD', replace=True)
			shapeListClean = self.getShapeList()

			# backup and remove previous auto backup shaders
			shaderFiles = []
			backupFileNames = []
			sceneFileBase = self.parseSceneFileName()
			fileName = cmds.file(query=True, sceneName=True)
			fileName = string.replace(fileName, '\\', '/')
			dirPath = os.path.dirname(fileName)
			shadersDir = (os.path.join(dirPath, 'shaderMan'))
			shadersDir = shadersDir.replace("\\", "/")
			log.debug('shadersDir: %s ' % shadersDir)
			backupFileName = self.parseSceneFileName()
			log.debug('backupFileName for import: %s ' % backupFileName)
			shaderFiles = sorted(glob.glob(os.path.join(shadersDir, '%sShaderMan_*.ma' % backupFileName)))
			log.debug('shaderFiles: %s ' % shaderFiles)
			for shaderFile in shaderFiles:
				if os.path.exists(shaderFile):
					utils.backupFile(shaderFile, verbose=False)

		# start the export
		print('\nExporting shaders...')

		# In interactive Character MTL mode, backup and remove old shader files
		if ((exportMode == 1) and (batchMode == 0)):
			charCategory = 'char'
			if ( os.path.split(cmds.workspace(q=True, fn=True))[1] == 'backlot' ):
				fileName = cmds.file(query=True, sceneName=True)
				fileName = string.replace(fileName, '\\', '/')
				if (re.match(r".*\/scenes\/master\/(?P<charCategory>\w+)\/.*", fileName)):
					f = re.match(r".*\/scenes\/master\/(?P<charCategory>\w+)\/.*", fileName)
					charCategory = f.group('charCategory')
			log.debug('charCategory is: %s' % charCategory)
			projectPath = cmds.workspace(q=True, fn=True)
			shaderFiles = glob.glob(os.path.join(projectPath, 'scenes', 'master', charCategory, autoCharName, 'shaders', 'shaderMan', '*.ma'))
			for shaderFile in shaderFiles:
				if os.path.exists(shaderFile):
					utils.backupFile(shaderFile, verbose=False)

		# grab renderer-specific settings
		self.renderSettingsTypes = self.setRenderSettingType()

		# clear out SG lists
		shaderList = cmds.ls(mat=True)
		log.debug('Clearing out SG lists...')
		for shader in shaderList:
			log.debug('shader: %s' % shader)
			try:
				shadingGroup = (cmds.listConnections(shader, t='shadingEngine')[0])
				cmds.deleteAttr(shadingGroup + '.renderLayer')
				cmds.deleteAttr(shadingGroup + '.shaderObjects')
				cmds.deleteAttr(shadingGroup + '.chars')
				cmds.deleteAttr(shadingGroup + '.shapeLiterals')
			except:
				pass

		# loop through layers and make list of objects and shaders
		layerAttrs = ''
		log.debug('Going to loop through renderLayersClean...')
		couldNotExport = ''
		for renderLayer in renderLayersClean:
			shaderExportList = []
			cmds.editRenderLayerGlobals(currentRenderLayer=renderLayer)
			cmds.select(cmds.editRenderLayerMembers( renderLayer, query=True, fn=True ), hi=True, replace=True) # select objects in layer
			layerMembers = cmds.ls(sl=True)
			log.debug('layerMembers: %s ' % layerMembers)

			for shape in shapeListClean:
				if (shape in layerMembers):
					log.debug('%s is in the layer %s' % (shape, renderLayer))
					
					# parse the shape name to determine character and prefix-stripped shape name
					log.debug('shape name to parse: %s' % (shape))
					parsedName = self.parseName(shape)
					if (parsedName == None):
						log.debug('Could not parse shape: %s \nPassing.' % shape)
						charName = '__LITERAL__'
					if (exportMode == 1):
						charName = autoCharName
					else:
						charName = parsedName['charName']
					shapeBaseName = parsedName['shapeBaseName']
					shapeLiteral = parsedName['shapeLiteral']
					shapeLiterals = ''
					shaderObjects = ''
					chars = ''
					charList = []
					log.debug('orig shape: %s ' % shape)
					try:
						shadingGroup = (cmds.listConnections(shape, t='shadingEngine')[0])
					except:
						print(' no shader connected to %s' % shape)
						pass
					log.debug('\n')
					log.debug("layer: %s, char: %s, shape: %s, shadingGroup: %s, shapeBaseName: %s, shapeLiteral: %s" % (renderLayer, charName, shape, shadingGroup, shapeBaseName, shapeLiteral))

					# append shape list to shaderObjects lists
					try:
						shaderObjects = cmds.getAttr('%s.shaderObjects' % shadingGroup)
					except:
						pass
					if (shape is not ''):
						if (shaderObjects == ''):
							shaderObjects = shapeBaseName + ',' + charName + ',' + renderLayer
						else:
							shaderObjects = shaderObjects + ' ' + shapeBaseName + ',' + charName + ',' + renderLayer
					shaderObjectsList = shaderObjects.split(' ')
					shaderObjectsList = list(set(shaderObjectsList)) # removes duplicates
					shaderObjects = ' '.join(shaderObjectsList)
					log.debug("shadingGroup: %s, new shaderObjects: %s, renderLayer: %s " % (shadingGroup, shaderObjects, renderLayer))
					if not (cmds.attributeQuery('shaderObjects', node=shadingGroup, exists=True)):
						cmds.addAttr(shadingGroup, dt='string', ln='shaderObjects' )
					cmds.setAttr('%s.shaderObjects' % shadingGroup, shaderObjects, type='string')
					
					# append shape literal list to shapeLiterals lists
					try:
						shapeLiterals = cmds.getAttr('%s.shapeLiterals' % shadingGroup)
					except:
						pass
					if (shape is not ''):
						if (shapeLiterals == ''):
							shapeLiterals = shapeLiteral + ',' + charName + ',' + renderLayer
						else:
							shapeLiterals = shapeLiterals + ' ' + shapeLiteral + ',' + charName + ',' + renderLayer
					shapeLiteralsList = shapeLiterals.split(' ')
					shapeLiteralsList = list(set(shapeLiteralsList)) # removes duplicates
					shapeLiterals = ' '.join(shapeLiteralsList)
					log.debug("shadingGroup: %s, shapeLiterals: %s, renderLayer: %s " % (shadingGroup, shapeLiterals, renderLayer))
					if not (cmds.attributeQuery('shapeLiterals', node=shadingGroup, exists=True)):
						cmds.addAttr(shadingGroup, dt='string', ln='shapeLiterals' )
					cmds.setAttr('%s.shapeLiterals' % shadingGroup, shapeLiterals, type='string')

					# append char to chars lists
					try:
						chars = cmds.getAttr('%s.chars' % shadingGroup)
					except:
						pass
					if (charName is not ''):
						if (chars == ''):
							chars = charName
						else:
							chars = chars + ' ' + charName
					if not (cmds.attributeQuery('chars', node=shadingGroup, exists=True)):
						cmds.addAttr(shadingGroup, dt='string', ln='chars' )
					charList = chars.split(' ')
					charList = list(set(charList)) # removes duplicates
					chars = ' '.join(charList)
					log.debug("shadingGroup: %s, new chars: %s " % (shadingGroup, chars))
					cmds.setAttr('%s.chars' % shadingGroup, chars, type='string')
					
					# add this shape's shader to the export list for this layer
					shaderExportList = shaderExportList + [shadingGroup]

					# set a renderLayer attribute on all of the shaders to export
					try:
						layerAttrs = cmds.getAttr('%s.renderLayer' % shadingGroup)
					except:
						pass
					if (renderLayer is not ''):
						if (layerAttrs == ''):
							layerAttrs = renderLayer
						else:
							layerAttrs = layerAttrs + ' ' + renderLayer
					log.debug("shadingGroup: %s, layerAttrs: %s " % (shadingGroup, layerAttrs))
					if not (cmds.attributeQuery('renderLayer', node=shadingGroup, exists=True)):
						cmds.addAttr(shadingGroup, dt='string', ln='renderLayer' )
					layerAttrList = layerAttrs.split(' ')
					layerAttrList = list(set(layerAttrList)) # removes duplicates
					layerAttrs = ' '.join(layerAttrList)
					cmds.setAttr('%s.renderLayer' % shadingGroup, layerAttrs, type='string')

			# print the list of shapes not found
			if (couldNotExport != []):
				print('The following shapes could not be found: %s' % couldNotExport)

			# build the list of shaders to export
			shaderExportList = list(set(shaderExportList)) # removes duplicates

			# export char name for export and info node
			if (exportMode == 1):
				exportFileBase = autoCharName
			elif (exportMode == 2):
				exportFileBase = self.parseSceneFileName()

			# clear out any existing layerInfo files
			infoNodes = cmds.ls('*ShaderMan_*_layerinfo', type='transform')
			for infoNode in infoNodes:
				cmds.delete(infoNode)

			# create a temp node to store render layer info
			layerInfoNode = cmds.createNode( 'transform', ss=True, name='%sShaderMan_%s_layerinfo' % (exportFileBase, renderLayer) )
			log.debug("layerInfoNodeName: %s" % layerInfoNode)
			for renderSettingsType in self.renderSettingsTypes:
				renderSettingsPair = renderSettingsType.split('__')
				try:
					cmds.addAttr(layerInfoNode, dt='string', ln=renderSettingsType)
					if (cmds.attributeQuery(renderSettingsType, node=layerInfoNode, exists=True)):
						cmds.setAttr( layerInfoNode + '.' + renderSettingsType, cmds.getAttr( renderSettingsPair[0] + '.' + renderSettingsPair[1] ), type='string' )
				except:
					print('Could not find render setting: %s. Skipping this render layer override.' % renderSettingsType)

			# export the shader file for this layer
			log.debug("layer: %s, shadingGroup list to export: %s " % (renderLayer, shaderExportList))
			if (shaderExportList != []):
				shadersDir = ''
				cmds.select(shaderExportList, r=True, ne=True)
				cmds.select(layerInfoNode, add=True)
				log.debug('selected stuff: %s ' % (cmds.ls(sl=True)))
				if (exportMode == 1):
					log.debug('exportMode 1')
					shadersDir = self.setShaderManDir(exportMode=exportMode, importMode=0, autoCharName=autoCharName)
				elif (exportMode == 0):
					log.debug('exportMode 0')
					shadersDir = self.setShaderManDir(exportMode=exportMode, importMode=0)
				else:
					log.debug('no exportMode specified')
					shadersDir = self.setShaderManDir(exportMode=exportMode, importMode=0)
				if not os.path.exists(shadersDir):
					log.debug('creating shaderMan directory')
					os.makedirs(shadersDir)
				outFile = (os.path.join(shadersDir, '%sShaderMan_%s.ma' % (exportFileBase, renderLayer)))
				outFile.encode('ascii','ignore')
				# write shaderMan file
				if os.path.exists(outFile):
					utils.backupFile(outFile, verbose=False)
				print('Writing shaderMan file: %s' % outFile )
				cmds.file(outFile, type='mayaAscii', exportSelected=True, force=True)

			# delete temp node
			cmds.delete(layerInfoNode)
			cmds.select(clear=True)

			# export vray render elements
			outFile = ''
			renderElements = []
			reExportList = []
			renderElements = cmds.ls(type='VRayRenderElement')
			for renderElement in renderElements:
				if (cmds.getAttr(renderElement + '.' + 'enabled') == 1):
					log.debug('render element: %s is enabled' % renderElement)
					reExportList.append(renderElement)
					cmds.select(renderElement, add=True)
			log.debug('reExportList: %s' % reExportList)
			if (shaderExportList != []):
				if (reExportList!= []):
					outFile = (os.path.join(shadersDir, '%sShaderManRE_%s.ma' % (exportFileBase, renderLayer)))
					outFile.encode('ascii','ignore')
					# write shaderMan file
					if os.path.exists(outFile):
						utils.backupFile(outFile, verbose=False)
					print('Writing shaderMan file: %s' % outFile )
					cmds.file(outFile, type='mayaAscii', exportSelected=True, force=True)
			if (couldNotExport != ''):
				cmds.confirmDialog( title='Alert', messageAlign='center', message=\
					'Warning: The following objects were NOT exported because a character name not be determined for them:\n\n%s\n\nThe shapes I could identify were exported though.' % couldNotExport
					, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )



	def importShaders(self, importMode=1, *args):
		'''
		filename = string to match for import file names
		layerMode = create new layer(s) or add to current layer (in the case of only one input layer),
			or add objects to matching layer names (or create if they don't exist) [options: new, current, merge]
		import modes:
		  1: From MTL Files (Auto)
		  2: From MTL Files (Select Character/Layers)
		  3: From Custom Files
		  4: From AutoBackup
		  
		'''
		sgLayerList = []
		shapes = ''
		shaderList = ''
		shapeList = []
		shape = ''
		prefixedShape = ''
		objectsNotFound = []
		charDirs = []
		shapeListClean = []
		fileContentsList = []
		shaderFiles = []

		# read the state of the UI buttons
		if (importMode == 4):
			log.debug('IMPORT MODE 4\n')
		else:
			importMode = cmds.radioButtonGrp(self.importMode, q=True, select=True)
		layerMode = cmds.radioButtonGrp(self.layerMode, q=True, select=True)
		selectedOnly = cmds.checkBoxGrp(self.selectedOnly, q=True, value1=True)
		postDeleteUnused = cmds.checkBoxGrp(self.postDeleteUnused, q=True, value1=True)
		looseMatchMode = cmds.checkBoxGrp(self.looseMatchMode, q=True, value1=True)
		literalMode = cmds.checkBoxGrp(self.literalMode, q=True, value1=True)
		importRenderSettings = cmds.checkBoxGrp(self.importRenderSettings, q=True, value1=True)
		charNameToReplace = cmds.textFieldGrp(self.charNameToReplace, q=True, text=True)
		charNameReplace = cmds.textFieldGrp(self.charNameReplace, q=True, text=True)
		replaceCharName = cmds.checkBoxGrp(self.replaceCharName, query=True, value1=True)
		prefsFile = ''
		renderSettingsChar = ''

		# Read prefs
		renderSettingsChar = self.readPrefs('renderSettingsChar')

		# fail if on masterLayer and New Layer option is off
		if (cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) == 'defaultRenderLayer') and (layerMode == 2):
			cmds.confirmDialog( title='Alert', messageAlign='center', message=
				'\"Current\" layer mode can not be used with masterLayer.  Please select a different layer or select a different layer mode. Doing nothing.'
				, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
			sys.exit()

		# get selected objects
		if (selectedOnly == True):
			shapeListClean = self.getShapeList()
		else:
			pass

		# determine list of shaderFiles
		# In Custom or MTL (Select) mode, expand the list of selected files from UI
		if ((importMode == 2) or (importMode == 3)):
			shaderFiles = []
			selectedFiles = self.getShaderFiles()
			# fail if no shader files are selected
			if (((importMode == 2) or (importMode == 3)) and (selectedFiles == None)):
				cmds.confirmDialog( title='Alert', messageAlign='center', message=\
					'No shader files selected. Doing nothing.'\
					, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
				sys.exit()
			for shaderFileName in selectedFiles:
				log.debug('shaderFileName: %s' % shaderFileName)
				shadersDir = self.setShaderManDir(exportMode=0, importMode=importMode)
				log.debug('shadersDir: %s/' % shadersDir)
				shaderFile = ('%s/%s.ma' % (shadersDir, shaderFileName))
				log.debug('shaderFile: %s/' % shaderFile)
				shaderFiles.append(shaderFile)
		# in MTL (Auto) mode, loop through all characters in the job...
		elif (importMode == 1):
			shaderFiles = []
			autoCharNames = []
			projectPath = cmds.workspace(q=True, fn=True)
			charDirs = glob.glob(os.path.join(projectPath, 'scenes', 'master', 'char', '*', 'shaders', 'shaderMan'))
			charDirs = list(set(charDirs)) # removes duplicates
			log.debug('charDirs: %s ' % charDirs)
			for charDir in charDirs:
				charDir = charDir.replace("\\", "/")
				log.debug('charDir: %s ' % charDir)
				m = re.match(r".*\/?.*\/scenes\/master\/char\/(?P<charDir>\w+)\/.*", charDir)
				charDir = m.group('charDir')
				if (charDir != renderSettingsChar):
					autoCharNames.append(charDir)
			autoCharNames.append(renderSettingsChar)
			

			log.debug('autoCharNames: %s ' % autoCharNames)
			for autoCharName in autoCharNames:
				log.debug('autoCharName: %s ' % autoCharName)
				# only import shaders for characters that are in the scene
				if ( (cmds.ls('*' + autoCharName + '*', tr=True) != []) or (cmds.ls('*' + autoCharName + '*', s=True) != []) or (self.parseFileName() == autoCharName) ):
					shadersDir = (os.path.join(projectPath, 'scenes', 'master', 'char', autoCharName, 'shaders', 'shaderMan'))
					#log.debug('shadersDir: %s ' % shadersDir)
					shaderFileGlob = glob.glob(os.path.join(shadersDir, '%sShaderMan_*.ma' % autoCharName))
					#log.debug('shaderFileGlob: %s ' % shaderFileGlob)
					shaderFiles.extend(shaderFileGlob)
					#log.debug('shader Files: %s ' % shaderFiles)
		# From AutoBackup mode
		elif (importMode == 4):
			log.debug('AUTO IMPORTING')
			shaderFiles = []
			literalMode = 1
			backupFileNames = []
			sceneFileBase = self.parseSceneFileName()
			fileName = cmds.file(query=True, sceneName=True)
			fileName = string.replace(fileName, '\\', '/')
			dirPath = os.path.dirname(fileName)
			shadersDir = (os.path.join(dirPath, 'shaderMan'))
			shadersDir = shadersDir.replace("\\", "/")
			log.debug('shadersDir: %s ' % shadersDir)
			backupFileName = self.parseSceneFileName()
			log.debug('backupFileName for import: %s ' % backupFileName)
			shaderFiles = sorted(glob.glob(os.path.join(shadersDir, '%sShaderMan_*.ma' % backupFileName)))
			log.debug('shaderFiles: %s ' % shaderFiles)

		# check if no shader files found
		if (shaderFiles == []):
			cmds.confirmDialog( title='Alert', messageAlign='center', message=\
				'No matching shader files found in character MTL directories. Doing nothing.'\
				, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
			sys.exit()

		# clear out any existing layerInfo files
		infoNodes = cmds.ls('*ShaderMan_*_layerinfo', type='transform')
		print('***Found infoNode: %s' % infoNodes)
		for infoNode in infoNodes:
			cmds.delete(infoNode)

		# start the import
		print('\nImporting shaders...')
		if (looseMatchMode == True):
			print('\n*** Using Loose Matching Mode.  Results could be unexpected. ***\n')

		# grab renderer-specific settings
		self.renderSettingsTypes = self.setRenderSettingType()

		# turn off masterLayer
		cmds.setAttr('defaultRenderLayer.renderable', 0)

		# list everything in the file
		fileContentsList = []
		fileContentsList.extend(cmds.ls(type='mesh'))
		fileContentsList.extend(cmds.ls(type='nurbsSurface'))
		fileContentsList.extend(cmds.ls(type='subdiv'))
		fileContentsList.extend(cmds.ls(type='aiStandIn'))

		# loop through shaderFiles
		cmds.progressWindow(title='Importing Shaders', maxValue=len(shaderFiles), status='Importing:', isInterruptable=True)
		for shaderFile in shaderFiles:
			# Check if the dialog has been cancelled
			if cmds.progressWindow(query=True, isCancelled=True):
				break

			# Check if end condition has been reached
			cmds.progressWindow(edit=True, step=1)

			print('Preparing to import shaderFile: %s/' % shaderFile)

			# figure out the layer name to create, create the new layer, and switch to that layer
			shaderFile = shaderFile.replace("\\", "/")
			m = re.match(r".*\/(?P<filebase>\w+)ShaderMan_(?P<renderLayer>\w+)", shaderFile)
			renderLayerType = m.group('renderLayer')
			filebase = m.group('filebase')
			log.debug('filebase: %s' % filebase)
			shaderFileRE = (os.path.join(shadersDir, '%sShaderManRE_%s.ma' % (filebase, renderLayerType))) # matching render elements file

			log.debug('renderLayerType: %s ' % renderLayerType)
			log.debug('shaderFileRE: %s ' % shaderFileRE)
			if (layerMode == 1):
				# new: create new layer(s)
				targetLayer = cmds.createRenderLayer(name=renderLayerType, empty=True)
				cmds.editRenderLayerGlobals(currentRenderLayer=targetLayer)
			elif (layerMode == 2):
				# current: add to current layer - only valid if one input layer is selected
				if len(selectedFiles) > 1:
					cmds.confirmDialog( title='Alert', messageAlign='center', message=\
						'\"Current\" layer mode can only be used with a single input file. Please select a different layer mode. Doing nothing.'
						, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
					sys.exit()
				targetLayer = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
			elif (layerMode == 3):
				# match: match input layer names to existing layers with the same name.  create layers if they don't exist.
				# If renderLayerType exists, switch to that layer.
				if (cmds.ls( renderLayerType, type='renderLayer')):
					cmds.editRenderLayerGlobals(currentRenderLayer=renderLayerType)
					targetLayer = renderLayerType
				# If it doesn't, create a new layer with that name, and switch to it.
				else:
					targetLayer = cmds.createRenderLayer(name=renderLayerType, empty=True)
					cmds.editRenderLayerGlobals(currentRenderLayer=targetLayer)
			else:
				log.error('Invalid layer mode.  Quitting..')
				sys.exit()
			
			# import the shader file
			print('Importing shaderFile: %s/' % shaderFile)
			try:
				importedNodes = cmds.file(shaderFile, i=True, type='mayaAscii', rpr=filebase, loadReferenceDepth='none', rnn=True )
			except:
				cmds.confirmDialog( title='Alert', messageAlign='center', message=\
					'Shader file %s not found. Doing nothing.' % shaderFile\
					, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
				sys.exit()

			'''
			# create importedShaders set
			importedShaderSet = cmds.sets(name='importedShaders', empty=True)
			cmds.sets(importedNodes, edit=True, addElement=importedShaderSet)
			'''

			# load render layer settings
			if (re.match(r".*\/(?P<shaderFileName>\w+)", shaderFile)):
				n = re.match(r'.*\/(?P<shaderFileName>\w+)', shaderFile)
				shaderFileName = n.group('shaderFileName')
				layerInfoNode = '%s_layerinfo' % shaderFileName
			if (importRenderSettings == True):
				for renderSettingsType in self.renderSettingsTypes:
					renderSettingsPair = renderSettingsType.split('__')
					try:
						if (cmds.attributeQuery(renderSettingsType, node=layerInfoNode, exists=True)):
							cmds.editRenderLayerAdjustment(renderSettingsPair[0] + '.' + renderSettingsPair[1])
							val = eval(cmds.getAttr( layerInfoNode + '.' + renderSettingsType ))
							cmds.setAttr( renderSettingsPair[0] + '.' + renderSettingsPair[1], val )
					except:
						print('Could not find render setting: %s. Skipping this render layer override.' % renderSettingsType)

			# limit shader search to what was imported in this run
			cmds.select(clear=True)
			cmds.select(importedNodes)
			shaderList = cmds.ls(selection=True, mat=True)

			# start reading all the shaders in the shader file, and connect them to each of the objects in the shaderObjects list
			#log.info('shaderList: %s' % shaderList)
			for shader in shaderList:
				#log.info('shader: %s' % shader)
				# find the connected SG group and start parsing shaderMan attributes
				if (cmds.listConnections(shader, t='shadingEngine')):
					shadingGroup = (cmds.listConnections(shader, t='shadingEngine')[0]) #TODO: what if there are multiple SGs connected?  this takes the first..
					if (cmds.attributeQuery('renderLayer', node=shadingGroup, exists=True)):
						sgLayers = cmds.getAttr('%s.renderLayer' % shadingGroup)
						sgLayerList = sgLayers.split(' ')
						if (cmds.attributeQuery('chars', node=shadingGroup, exists=True)):
							chars = cmds.getAttr('%s.chars' % shadingGroup)
							charList = chars.split(' ')
							# now that you know the characters you want, filter out unwanted layers to import
							for charPossible in charList:
								#log.info('charPossible: %s' % charPossible)
								for sgLayer in sgLayerList:
									#log.info('sgLayer: %s' % sgLayer)
									if (sgLayer == renderLayerType):
										# read the shaderObjects attribute to find base shape names to attach to
										shapeFound = False
										if (literalMode == 1):
											shapes = cmds.getAttr('%s.shapeLiterals' % shadingGroup)
										else:
											shapes = cmds.getAttr('%s.shaderObjects' % shadingGroup)
										shapeTripletList = shapes.split(' ')
										shapeTripletList = list(set(shapeTripletList)) # removes duplicates
										#log.debug('shapeTripletList: %s' % shapeTripletList)
										for triplet in shapeTripletList:
											log.info('triplet: %s' % triplet)
											shapeTriplet = triplet.split(',')
											shape = shapeTriplet[0] # use dict?
											charName = shapeTriplet[1] # use dict?
											layerInclude = shapeTriplet[2]
											if (layerInclude != sgLayer):
												log.debug('shape not in layer. skipping.')
												continue

											# the final list of shapes to act on
											shapeListExpanded = []

											if (literalMode == 1):
												# filter for items in the current maya file
												shapeMatch = re.compile(shape)
												for mayaItem in fileContentsList:
													if (shapeMatch.match(mayaItem)):
														shapeListExpanded.extend([mayaItem])
											else:
												if (replaceCharName == 1):
													if (charNameToReplace == charName):
														charName = charNameReplace

												suffixList = ['', 'Deformed']

												for suffix in suffixList:
													# setup shape name patterns to match
													patternsList = [\
														(re.compile('(%s%s)' % (shape, suffix))), \
														(re.compile('(geo_%s%s)' % (shape, suffix))), \
														(re.compile('%s.*?_geo_%s%s' % (charName, shape, suffix))), \
														(re.compile('anm_%s.*?_geo_%s%s' % (charName, shape, suffix))), \
														(re.compile('anm_%s%s%s' % (charName, shape, suffix))), \
														(re.compile('anm_%s_%s%s' % (charName, shape, suffix))), \
														(re.compile('%s_%s%s' % (charName, shape, suffix))) ]

													# "Loose" Name Matching - to help with non-standard object names
													if (looseMatchMode == True):
														patternsList.extend([(re.compile('anm_%s.*?%s.*' % (charName, shape)))])

													# filter for items in the current maya file
													for mayaItem in fileContentsList:
														for pattern in patternsList:
															if (pattern.match(mayaItem)):
																shapeListExpanded.extend([mayaItem])

											if (selectedOnly == True):
												shapeListExpanded = frozenset(shapeListClean).intersection(shapeListExpanded)
											else:
												pass

											# Process the found shapes
											log.debug('shapeListExpanded: %s' % shapeListExpanded)

											if not (shapeListExpanded == []):
												shapeFound = True
												for shapeExpanded in shapeListExpanded:
													log.debug('charName: %s, layer: %s, shapeExpanded: %s, shadingGroup: %s ' % (charName, targetLayer, shapeExpanded, shadingGroup))
													log.debug('cmds.editRenderLayerMembers(\'%s\', \'%s\', noRecurse=True)' % (targetLayer, shapeExpanded) )
													cmds.editRenderLayerMembers(targetLayer, shapeExpanded, noRecurse=True)
													log.debug('cmds.sets(\'%s\', e=True, forceElement=\'%s\')' % (shapeExpanded, shadingGroup) )
													cmds.sets(shapeExpanded, e=True, forceElement=shadingGroup )
												
											if (shapeFound == False):
												objectsNotFound = objectsNotFound + [shape]
						else:
							pass

					else:
						pass
				else:
					pass

			# delete layerInfo node
			try:
				cmds.delete(layerInfoNode)
			except:
				pass

			# list shapes not found in scene
			if not (objectsNotFound == []):
				print('The following objects were not found: %s' % objectsNotFound)

			# import vray render elements #TODO: support for mentalRay
			reImportItems = []
			reImportCleanupList = []
			if (os.path.exists(shaderFileRE)):
				reImportItems = cmds.file(shaderFileRE, i=True, type='mayaAscii', rpr='VRAY_RE_TEMP', loadReferenceDepth='none', rnn=True )
				log.debug('reImportItems: %s' % reImportItems)
				for reImportItem in reImportItems:
					log.debug('reImportItem: %s' % reImportItem)
					prefix = 'VRAY_RE_TEMP_'
					if reImportItem.startswith(prefix):
						reImportCleanupList.append(reImportItem)
						# if a duplicate render element was imported, enable the original in this layer
						if (cmds.objectType( reImportItem ) == 'VRayRenderElement'):
							reBaseName = reImportItem[len(prefix):]
							log.debug('base name is %s' % reBaseName)
							cmds.editRenderLayerAdjustment(reBaseName + '.enabled')
							cmds.setAttr(reBaseName + '.enabled', 1)
					else:
						# if the imported render element is not a duplicate, disable it on base layer and override enable on this layer
						if (cmds.objectType( reImportItem ) == 'VRayRenderElement'):
							cmds.setAttr(reImportItem + '.enabled', 0)
							cmds.editRenderLayerAdjustment(reImportItem + '.enabled')
							cmds.setAttr(reImportItem + '.enabled', 1)

			# delete duplicate render element imports
			if (reImportCleanupList != []):
				cmds.delete(reImportCleanupList)
		cmds.progressWindow(endProgress=1)

		# delete unused shaders
		if (postDeleteUnused == True):
			self.deleteUnused()
		print('Done!')

	def textreplace(self, file_path, pattern, subst):
		#Create temp file
		fh, abs_path = mkstemp()
		new_file = open(abs_path,'w')
		old_file = open(file_path)
		for line in old_file:
			if (re.match(r".*rfn \"anmRN\" \"(?P<anmFilePath>.*)", line)):
				m = re.match(r".*rfn \"anmRN\" \"(?P<anmFilePath>.*)", line)
				anmFilePath = m.group('anmFilePath')
				log.debug('anmFilePath: %s' % anmFilePath)
				line = re.sub(anmFilePath, subst, line)
			new_file.write(line)
		#close temp file
		new_file.close()
		os.close(fh)
		old_file.close()
		#Remove original file
		os.remove(file_path)
		#Move new file
		shutil.move(abs_path, file_path)


	def repairFile(self, *args):
		# popup a path chooser
		self.oldAnimFile = self.animFilePopup()[0].encode('ascii','ignore')
		log.debug('self.oldAnimFile: %s' % self.oldAnimFile)
		
		# workshop the file
		mel.eval('lgtFiler "saveWorkshop" `workspace -q -fn`  `file -q -shn -sn` "ma" "lgt" 0 0 0 1;')
		fileName = cmds.file(query=True, sceneName=True)
		log.debug('fileName: %s' % fileName)

		# close the file
		cmds.file(new=True, force=True)

		# textreplace the path to the anim reference and save as a new file
		prefix = ''
		suffix = '\";'
		self.textreplace(fileName, '.*\"anmRN\" \".*\.ma', ('%s%s%s') % (prefix, self.oldAnimFile, suffix))

		# open the textreplaced file
		cmds.file(fileName, open=True, force=True)
		log.debug('file opened!')

		# export shaders
		self.exportShaders(exportMode=2)
		# build the list of refs
		refFileDict = {}
		refFilePaths = cmds.file(query=True, reference=True)
		i = 0
		print('refFilePaths: %s' % refFilePaths)
		for refFile in refFilePaths:
			refFilePrefix = (cmds.file(refFile, query=True, rfn=True)).rstrip('RN')
			refFile = string.replace(refFile, '\\', '/')
			print refFile
			refFileDict[refFilePrefix] = refFile
		print refFileDict

		# remove anm ref
		print('Removing anm ref...')
		for refFilePrefix in refFileDict:
			print('%s : %s' % ( refFilePrefix, refFileDict[refFilePrefix]))
			if refFilePrefix == 'anm':
				print('removing reference: %s' % refFileDict[refFilePrefix])
				cmds.file(refFileDict[refFilePrefix], removeReference=True) 

		# reference the anim back in
		print('Re-referencing anm master...')
		shotNum = ''
		for refFilePrefix in refFileDict:
			if ((refFilePrefix == 'anm') and (re.match(r".*\/(?P<shotNum>\w+)_anmRef\..*", refFileDict[refFilePrefix]))):
				m = re.match(r".*\/(?P<shotNum>\w+)_anmRef\..*", refFileDict[refFilePrefix])
				shotNum = m.group('shotNum')
			elif ((refFilePrefix == 'anm') and (re.match(r".*\/(?P<shotNum>\w+)_anm\..*", refFileDict[refFilePrefix]))):
				m = re.match(r".*\/(?P<shotNum>\w+)_anm\..*", refFileDict[refFilePrefix])
				shotNum = m.group('shotNum')
			if (shotNum != ''):
				print('shotNum: %s' % shotNum)
				projectPath = cmds.workspace(q=True, fn=True)
				anmMasterFile = glob.glob(os.path.join(projectPath, 'scenes', shotNum, 'anm', '%s_anm.ma') % shotNum)
				cmds.file(anmMasterFile, reference=True, type='mayaAscii', groupLocator=True, loadReferenceDepth='all', mergeNamespacesOnClash=False, rpr=refFilePrefix, options='v=0')
			else:
				pass
		# delete unused shaders
		self.deleteUnused()

		# import from the backup file
		self.importShaders(importMode=4)

	# delete unused shaders
	def deleteUnused(self):
		mel.eval('source cleanUpScene')
		mel.eval('putenv "MAYA_TESTING_CLEANUP" "1"')
		mel.eval('scOpt_performOneCleanup( { "shaderOption" } )')
		mel.eval('putenv "MAYA_TESTING_CLEANUP" ""')


	# for export, parse the name of the current shape, to determine the character and shape base name
	def parseName(self, inputString):
		charName = ''
		shapeBaseName = ''
		shapeLiteral = ''
		shapeLiteral = inputString
		# strip long (fully qualified) names down to short names
		if (re.match(r".*\|(?P<inputStringShort>\w+)", inputString)):
			m = re.match(r".*\|(?P<inputStringShort>\w+)", inputString)
			inputString = m.group('inputStringShort')

		# standard names in lighting files
		if (re.match(r"(anm_)?(?P<charName>\w+?)\d*_geo_(?P<shapeBaseName>\w+)", inputString)):
			m = re.match(r"(anm_)?(?P<charName>\w+?)\d*_geo_(?P<shapeBaseName>\w+)", inputString)
			shapeBaseName = m.group('shapeBaseName')
			charName = m.group('charName')
		# in anm files
		elif (re.match(r"(anm_)?(?P<charName>\w+?)\d*_(?P<shapeBaseName>\w+)", inputString)):
			m = re.match(r"(anm_)?(?P<charName>\w+?)\d*_(?P<shapeBaseName>\w+)", inputString)
			shapeBaseName = m.group('shapeBaseName')
			charName = m.group('charName')
		# to support anm objects that get run through fx
		elif (re.match(r"(anm_fx_)?(?P<charName>\w+?)\d*_(?P<shapeBaseName>\w+)", inputString)):
			m = re.match(r"(anm_fx_)?(?P<charName>\w+?)\d*_(?P<shapeBaseName>\w+)", inputString)
			shapeBaseName = m.group('shapeBaseName')
			charName = m.group('charName')

		# in rig files, no prefix - parse name of maya file instead
		elif (re.match(r"geo_(?P<shapeBaseName>\w+)", inputString)):
			m = re.match(r"geo_(?P<shapeBaseName>\w+)", inputString)
			shapeBaseName = m.group('shapeBaseName')
			charName = self.parseFileName()
		# in geo files, no prefix - parse name of maya file instead
		else:
			m = re.match(r"(?P<shapeBaseName>\w+)", inputString)
			shapeBaseName = m.group('shapeBaseName')
			charName = self.parseFileName()

		log.debug('input string: %s' % inputString)
		log.debug('shape base name: %s' % shapeBaseName)
		log.debug('shape literal name: %s' % shapeLiteral)

		if charName is None:
			log.debug('could not find character name for shape: %s' % inputString)
			charName = '__LITERAL__'
		log.debug('char name: %s' % charName)
		parsedName = {'charName':charName, 'shapeBaseName':shapeBaseName, 'shapeLiteral':shapeLiteral }
		return parsedName


	# parse the name of the current maya file, for character names
	def parseFileName(self):
			fileName = cmds.file(query=True, sceneName=True)
			if (re.match(r".*\/(?P<charName>\w+)_geo", fileName)):
				f = re.match(r".*\/(?P<charName>\w+)_geo", fileName)
				charName = f.group('charName')
				return charName
			if (re.match(r".*\/(?P<charName>\w+)_mtl", fileName)):
				f = re.match(r".*\/(?P<charName>\w+)_mtl", fileName)
				charName = f.group('charName')
				return charName
			if (re.match(r".*\/.*_(?P<charName>\w+)_turntable", fileName)):
				f = re.match(r".*\/.*_(?P<charName>\w+)_turntable", fileName)
				charName = f.group('charName')
				return charName
			else:
				charName = ''


	# parse the name of the current maya file, for lgt workshop file names
	def parseSceneFileName(self):
			log.debug('PARSE SCENE FILE NAME')
			fileName = cmds.file(query=True, sceneName=True)
			fileName = string.replace(fileName, '\\', '/')
			if (re.match(r".*\/lgt\/workshop\/.*_(?P<sceneFileName>\w+)\..*", fileName)):
				f = re.match(r".*\/lgt\/workshop\/.*_(?P<sceneFileName>\w+)\..*", fileName)
				sceneFileName = f.group('sceneFileName')
				log.debug('sceneFileName lgt: %s' % sceneFileName)
				return sceneFileName
			elif (re.match(r".*\/(?P<sceneFileName>\w+)", fileName)):
				f = re.match(r".*\/(?P<sceneFileName>\w+)", fileName)
				sceneFileName = f.group('sceneFileName')
				log.debug('sceneFileName non lgt: %s' % sceneFileName)
				return sceneFileName
			else:
				log.debug('scene file name not parseable')
				sceneFileName = ''


	# parse the name of the current maya file, for lgt workshop file names
	def parseShotNum(self):
			log.debug('PARSE SHOT NUMBER')
			fileName = cmds.file(query=True, sceneName=True)
			fileName = string.replace(fileName, '\\', '/')
			if (re.match(r".*\/scenes\/shot(?P<shotNum>\d+)\/.*", fileName)):
				f = re.match(r".*\/scenes\/shot(?P<shotNum>\d+)\/.*", fileName)
				shotNum = f.group('shotNum')
				log.debug('shotNum: %s' % shotNum)
				return shotNum
			else:
				log.debug('scene file name not parseable')
				shotNum = ''


	def setShaderManDir(self, exportMode=0, importMode=0, autoCharName=''):
		shadersDir = ''
		log.debug('setShaderManDir...')
		projectPath = cmds.workspace(q=True, fn=True)
		log.debug('projectPath: %s' % projectPath)
		if (importMode == 2):
			autoCharName = cmds.textScrollList(self.fileScrollList, q=True, si=True)[0]
			log.debug('auto char name: %s' % autoCharName)
		log.debug('exportMode: %s' % exportMode)
		if ((exportMode == 1) or ((importMode == 1) or (importMode == 2))):
			# character-specific directory
			charCategory = 'char'
			if ( os.path.split(cmds.workspace(q=True, fn=True))[1] == 'backlot' ):
				fileName = cmds.file(query=True, sceneName=True)
				fileName = string.replace(fileName, '\\', '/')
				if (re.match(r".*\/scenes\/master\/(?P<charCategory>\w+)\/.*", fileName)):
					f = re.match(r".*\/scenes\/master\/(?P<charCategory>\w+)\/.*", fileName)
					charCategory = f.group('charCategory')
			log.debug('charCategory is: %s' % charCategory)
#############- -------------- fix below paths			
			shadersDir = (os.path.join(projectPath, 'scenes', 'master', charCategory, autoCharName, 'shaders', 'shaderMan'))
			log.debug('shadersDir: %s' % shadersDir)
		elif (exportMode == 2):
			# AutoBackup mode
			sceneFileBase = self.parseSceneFileName()
			fileName = cmds.file(query=True, sceneName=True)
			fileName = string.replace(fileName, '\\', '/')
			dirPath = os.path.dirname(fileName)
			shadersDir = (os.path.join(dirPath, 'shaderMan'))
			shadersDir = shadersDir.replace("\\", "/")
		else:
			# shared directory
			shadersDir = (os.path.join(projectPath, 'shaders', 'shaderMan'))

		return shadersDir


	def listShaderFiles(self, importMode=1):
		log.debug('listShaderFiles...')
		# glob input files
		shaderFiles = []
		shaderFileNames = []
		shaderFileBaseNames = []
		shaderFileDict = {}
		shaderFileGlob = []
		shaderFilesClean = []
		try:
			importMode = cmds.radioButtonGrp(self.importMode, query=True, select=True)
		except:
			importMode = 1
		log.debug('importMode: %s' % importMode)

		if (importMode == 3):
			shadersDir = self.setShaderManDir(importMode=3)
			log.debug('shot to shot shadersDir: %s' % shadersDir)
			shaderFileGlob = glob.glob(os.path.join(shadersDir, '*ShaderMan_*.ma'))
			shaderFiles = sorted(shaderFileGlob)
		else:
			# in From MTL mode, loop through all characters in the job...
			autoCharNames = []
			projectPath = cmds.workspace(q=True, fn=True)
##################### ------------ fix the below paths	
			shaderDirs = glob.glob(os.path.join(projectPath, 'scenes', 'master', 'char', '*', 'shaders', 'shaderMan'))
			log.debug('shaderDirs: %s' % shaderDirs)
			renderSettingsChar = ''

			# Read prefs
			renderSettingsChar = self.readPrefs('renderSettingsChar')

			for shaderDir in shaderDirs:
				shaderDir = shaderDir.replace("\\", "/")
				log.debug('MTL shaderDir: %s ' % shaderDir)
				m = re.match(r".*\/?.*\/scenes\/master\/char\/(?P<shaderDir>\w+)\/.*", shaderDir)
				shaderDir = m.group('shaderDir')
				autoCharNames.append(shaderDir)

			log.debug('autoCharNames: %s ' % autoCharNames)
			for autoCharName in autoCharNames:
				shadersDir = (os.path.join(projectPath, 'scenes', 'master', 'char', autoCharName, 'shaders', 'shaderMan'))
				shadersDir = shadersDir.replace("\\", "/")
				log.debug('character: %s shadersDir: %s ' % (autoCharName, shadersDir))
				shaderFileGlob = glob.glob(os.path.join(shadersDir, '%sShaderMan_*.ma' % autoCharName))
				log.debug('shaderFileGlob: %s ' % shaderFileGlob)
				shaderFiles.extend(shaderFileGlob)
				log.debug('shader Files: %s ' % shaderFiles)
			
		# strip full shader file paths down to file names with no extension
		for shaderFile in shaderFiles:
			shaderFile = shaderFile.replace("\\", "/")
			if (re.match(r".*\/(?P<shaderFileName>\w+)", shaderFile)):
				log.debug('shaderFile: %s ' % shaderFile)
				n = re.match(r'.*\/(?P<shaderFileName>\w+)', shaderFile)
				shaderFileName = n.group('shaderFileName')
				shaderFileNames.append(shaderFileName)

		# parse file base names from layer names
		for shaderFileName in shaderFileNames:
			shaderFileName = shaderFileName.replace("\\", "/")
			m = re.match(r"(?P<filebase>\w+)ShaderMan_(?P<renderLayer>\w+)", shaderFileName)
			filebase = m.group('filebase')
			renderLayer = m.group('renderLayer')
			# create a new key for each basename
			try:
				shaderFileDict[filebase]
			except:
				# if this filebase is new..
				shaderFileDict[filebase] = []
				shaderFileBaseNames.append(filebase)
			templist = shaderFileDict[filebase]
			templist.append(renderLayer)

		log.debug('shaderFileDict: %s ' % shaderFileDict)
		log.debug('shaderFileBaseNames: %s ' % shaderFileBaseNames)
		return (shaderFileDict,shaderFileBaseNames)


	def refreshFileBaseList(self, importMode=1, *args):
		log.debug('refreshFileBaseList...')
		cmds.textScrollList(self.fileScrollList, e=True, removeAll=True)
		cmds.textScrollList(self.layerScrollList, e=True, removeAll=True)
		shaderFileBaseNames = sorted(self.listShaderFiles(importMode=importMode)[1])
		cmds.textScrollList( self.fileScrollList, e=True, append=shaderFileBaseNames )


	def refreshLayerList(self, importMode=1, *args):
		log.debug('refreshLayerList...')
		cmds.textScrollList(self.layerScrollList, e=True, removeAll=True)
		shaderFileBase = None
		try:
			shaderFileBase = cmds.textScrollList(self.fileScrollList, query=True, si=True)[0]
		except:
			pass
		if (shaderFileBase != None):
			log.debug('refresh layer shaderFileBase: %s' % shaderFileBase )
			log.debug('refresh layer shaderFileDict: %s' % self.listShaderFiles(importMode=importMode)[0])
			shaderLayerNames = sorted(self.listShaderFiles(importMode=importMode)[0][shaderFileBase])
			cmds.textScrollList( self.layerScrollList, e=True, append=shaderLayerNames )


	# Export Mode Only
	def toggleFileBase(self, *args):
		log.debug('toggleFileBase...')
		fileBaseEnabled = cmds.textFieldGrp(self.exportFileBase, query=True, enable=1)
		if (fileBaseEnabled == 1):
			cmds.textFieldGrp(self.exportFileBase, edit=True, enable=0)
		else:
			cmds.textFieldGrp(self.exportFileBase, edit=True, enable=1)


	# Import Mode Only
	def toggleImportMode(self, *args):
		log.debug('toggleImportMode...')
		importMode = cmds.radioButtonGrp(self.importMode, query=True, select=True)
		if (importMode == 1):
			cmds.textScrollList(self.fileScrollList, edit=True, enable=0)
			cmds.textScrollList(self.layerScrollList, edit=True, enable=0)
			cmds.text(self.filesText, edit=True, label='Characters:', align='left', enable=0 )
			cmds.radioButtonGrp(self.layerMode, edit=True, enable2=0)
			cmds.radioButtonGrp(self.layerMode, edit=True, select=3)
			self.refreshFileBaseList()
		if (importMode == 2):
			cmds.textScrollList(self.fileScrollList, edit=True, enable=1)
			cmds.textScrollList(self.layerScrollList, edit=True, enable=1)
			cmds.text(self.filesText, edit=True, label='Characters:', align='left', enable=1 )
			cmds.radioButtonGrp(self.layerMode, edit=True, enable2=1)
			self.refreshFileBaseList()
		if (importMode == 3):
			cmds.textScrollList(self.fileScrollList, edit=True, enable=1)
			cmds.textScrollList(self.layerScrollList, edit=True, enable=1)
			cmds.text(self.filesText, edit=True, label='Files:', align='left', enable=1 )
			cmds.radioButtonGrp(self.layerMode, edit=True, enable2=1)
			self.refreshFileBaseList()

	def toggleReplaceCharName(self, *args):
		log.debug('toggleReplaceCharName...')
		replaceCharName = cmds.checkBoxGrp(self.replaceCharName, query=True, value1=True)
		if (replaceCharName == 1):
			cmds.textFieldGrp(self.charNameToReplace, edit=True, enable=1)
			cmds.textFieldGrp(self.charNameReplace, edit=True, enable=1)
		else:
			cmds.textFieldGrp(self.charNameToReplace, edit=True, enable=0)
			cmds.textFieldGrp(self.charNameReplace, edit=True, enable=0)


	def getShaderFiles(self):
		log.debug('getShaderFiles...')
		shaderFiles = []
		try:
			shaderFileBaseName = cmds.textScrollList(self.fileScrollList, q=True, si=True)[0]
		except:
			cmds.confirmDialog( title='Alert', messageAlign='center', message=\
				'No ShaderMan file selected for import. Please select a file to import from. Doing nothing.'
				, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
			sys.exit()

		shaderFileLayerNames = cmds.textScrollList(self.layerScrollList, q=True, si=True)
		if (shaderFileLayerNames == None):
			cmds.confirmDialog( title='Alert', messageAlign='center', message=\
				'No layers selected for import. Please select at least one layer. Doing nothing.'
				, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
			sys.exit()
		shaderFileBaseName.encode('ascii','ignore')
		for shaderFileLayerName in shaderFileLayerNames:
			shaderFileLayerName.encode('ascii','ignore')
			shaderFiles.append(shaderFileBaseName + 'ShaderMan_' + shaderFileLayerName)

		log.debug('shaderFiles: %s' % shaderFiles)

		return shaderFiles


	def getShapeList(self):
		# build the list of selected objects
		shapeListClean = []
		cmds.select(hi=True)
		shapeList = cmds.ls(sl=True, s=True)
		if not shapeList:
			cmds.confirmDialog( title='Alert', messageAlign='center', message=\
				'No objects selected. Doing nothing.'\
				, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
			sys.exit()
		for shape in shapeList:
			if ( (cmds.objectType(shape, isType='mesh')) or (cmds.objectType(shape, isType='nurbsSurface')) or (cmds.objectType(shape, isType='subdiv')) or (cmds.objectType(shape, isType='aiStandIn')) ):
				shapeListClean.append(shape)
		log.debug('shape list: %s ' % shapeListClean)
		cmds.select(clear=True)

		return shapeListClean


	def setRenderSettingType(self):
		renderer = cmds.getAttr('defaultRenderGlobals.currentRenderer')
		log.debug('renderer: %s' % renderer)
		renderSettingsTypes = []
		if (renderer == 'vray'):
			renderSettingsTypes = [
				'vraySettings__dmcMinSubdivs',
				'vraySettings__dmcMaxSubdivs',
				'vraySettings__dmcs_adaptiveAmount',
				'vraySettings__dmcs_adaptiveThreshold',
				'vraySettings__dmcs_adaptiveMinSamples',
				'vraySettings__dmcs_subdivsMult',
				'vraySettings__fixedSubdivs',
				'vraySettings__giOn',
				'vraySettings__relements_enableall',
				'vraySettings__samplerType'
				]
		elif (renderer == 'mentalRay'):
			renderSettingsTypes = [
				'miDefaultFramebuffer__datatype',
				'miDefaultOptions__forceMotionVectors',
				'miDefaultOptions__motionBlur',
				'miDefaultOptions__rayTracing',
				'miDefaultOptions__shutter',
				'miDefaultOptions__shutterDelay'
				]
		elif (renderer == 'arnold'):
			renderSettingsTypes = [
				'defaultArnoldRenderOptions__AASamples',
				'defaultArnoldRenderOptions__GIDiffuseSamples',
				'defaultArnoldRenderOptions__GIGlossySamples',
				'defaultArnoldRenderOptions__GIRefractionSamples',
				'defaultArnoldRenderOptions__sssBssrdfSamples',
				'defaultArnoldRenderOptions__volumeIndirectSamples',
				'defaultArnoldRenderOptions__GITotalDepth',
				'defaultArnoldRenderOptions__GIDiffuseDepth',
				'defaultArnoldRenderOptions__GIGlossyDepth',
				'defaultArnoldRenderOptions__GIReflectionDepth',
				'defaultArnoldRenderOptions__GIRefractionDepth',
				'defaultArnoldRenderOptions__autoTransparencyDepth'
				]
		else:
			renderSettingsTypes = []

		return renderSettingsTypes

	def autoExportAll(self, *args):
		mayaPath = os.path.join(os.environ['MAYA_LOCATION'], 'bin', 'mayapy')
		scriptPath = os.path.join(os.environ['MAYA_ROOT'], 'scripts', 'lgt_scripts', 'shaderMan.py')

		autoCharNames = []
		projectPath = cmds.workspace(q=True, fn=True)
		charDirs = glob.glob(os.path.join(projectPath, 'scenes', 'master', 'char', '*', 'mtl', 'workshop'))
		for charDir in charDirs:
			charDir = charDir.replace("\\", "/")
			log.debug('charDir: %s' % charDir)
			m = re.match(r".*\/?.*\/scenes\/master\/char\/(?P<charDir>\w+)\/.*", charDir)
			charDir = m.group('charDir')
			autoCharNames.append(charDir)
		print('autoCharNames: %s ' % autoCharNames)

		# set project path and renderer
		projectPath = cmds.workspace(q=True, fn=True)
		renderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")

		for char in autoCharNames:
			print ('exporting character: %s' % char)
			subprocess.Popen(['xterm', '-e', mayaPath, scriptPath, char, projectPath, renderer]) # to run in the background in a popup shell window

	def getPrefsFile(self):
		# set path to config file
		shadersDir = self.setShaderManDir(importMode=3)
		prefsFile = (os.path.join(shadersDir, 'shaderManPrefs.cfg' ))

		# Create directories and config file if they don't exist
		if not os.path.exists(shadersDir):
			os.makedirs(shadersDir)
		if not os.path.exists(prefsFile):
			open(prefsFile, 'a').close()

		return prefsFile

	def savePrefs(self, *args):
		# Set and save prefs
		prefsFile = self.getPrefsFile()
		log.debug('prefsFile: %s' % prefsFile)
		# Set config file value
		config = ConfigParser.ConfigParser()
		config.add_section('Prefs')
		try:
			renderSettingsChar = cmds.textScrollList(self.prefsFileScrollList, q=True, si=True)[0]
			log.debug('renderSettingsChar: %s' % renderSettingsChar)
			config.set('Prefs', 'renderSettingsChar', renderSettingsChar)
		except:
			print ('No render settings character specified.')

		# Writing config file
		with open(prefsFile, 'wb') as configfile:
			config.write(configfile)

		# Close render settings popup window
		try:
			cmds.deleteUI(self.renderCharPopupName)
		except:
			pass

	def readPrefs(self, prefName):
		prefsFile = self.getPrefsFile()
		if (os.path.isfile(prefsFile) == True):
			log.debug('prefsFile path: %s' % prefsFile)
			config = ConfigParser.ConfigParser()
			config.read(prefsFile)
			try:
				prefName = config.get('Prefs', prefName, 0)
			except:
				print 'shaderMan prefs file is blank.'
		else:
			print 'No shaderMan prefs file found. Using defaults.'

		return prefName

	def renderSettingsCharPopup(self, *args):
		if ( os.path.split(cmds.workspace(q=True, fn=True))[1] != 'backlot' ):
			self.renderCharPopupName = 'renderSettingsCharPopup'
			self.title = 'Render Settings Character'

			# Begin creating the UI
			if (cmds.window(self.renderCharPopupName, q=1, exists=1)): cmds.deleteUI(self.renderCharPopupName)
			self.window = cmds.window(self.renderCharPopupName, title=self.title)
			self.column = cmds.columnLayout()

			# glob shader files
			shaderFileNames = []
			shaderFileBaseNames = sorted(self.listShaderFiles(importMode=1)[1])

			# read prefs
			self.renderSettingsChar = self.readPrefs('renderSettingsChar')
			if (self.renderSettingsChar == "renderSettingsChar"):
				print('No render settings character specified. Last one wins.')

			self.prefsFileScrollList = cmds.textScrollList( numberOfRows=12, allowMultiSelection=False, append=shaderFileBaseNames, selectCommand=self.refreshLayerList, enable=1, si=self.renderSettingsChar )
			self.savePrefsButton = cmds.button( label='Set Render Settings Character', command=self.savePrefs)

			cmds.window(self.window, e=True, w=250, h=400, sizeable=0)
			cmds.showWindow(self.window)

	def animFilePopup(self, *args):
		if ( os.path.split(cmds.workspace(q=True, fn=True))[1] != 'backlot' ):
			self.animFilePopupName = 'animFilePopup'
			self.title = 'Anim File'

			# Begin creating the UI
			if (cmds.fileDialog2(self.animFilePopupName, q=1, exists=1)): cmds.deleteUI(self.animFilePopupName)
			projectPath = cmds.workspace(q=True, fn=True)
			shotNum = ''
			shotNum = self.parseShotNum()
################# --------------------- fix these paths
			anmVersionsDir = (os.path.join(projectPath, 'scenes', 'shot%s', 'anm', 'versions') % shotNum)
			anmVersionsDir = string.replace(anmVersionsDir, '\\', '/')
			log.debug('anmVersionsDir: %s' % anmVersionsDir)
			self.oldAnimFile = cmds.fileDialog2(startingDirectory=anmVersionsDir, fileMode=1)

			log.debug('oldAnimFile: %s' % self.oldAnimFile)
			return self.oldAnimFile


	def renderSettingsCheckBoxChange(self, *args):
		# Toggle name to be enabled / disabled
		enableField = True
		importMode = cmds.radioButtonGrp(self.importMode, query=True, select=True)
		# Disable Render Settings Character popup if Import Render Settings is unchecked, or if you're not in From MTL (Auto) Mode
		if cmds.checkBoxGrp(self.importRenderSettings, q=True, v1=True) != 1:
			pass
		elif (importMode != 1):
			pass
		else:
			self.renderSettingsCharPopup()


# to run in a shell (this is the code that gets run when subprocess is called)
if __name__ == '__main__':
	import sys
	import chrlx_scripts.filer as filer

	char = ''
	projectPath = ''
	char = sys.argv[1]
	projectPath = sys.argv[2]
	renderer = sys.argv[3]

	if len(sys.argv) < 4:
		print 'hey, not enough arguments! exiting.'
		sys.exit(-1)
	import maya.standalone as std
	std.initialize(name='python')

	import maya.mel as mel
	mel.eval('setProject("%s")' % projectPath)

	# backup and remove all old shaderMan files
	shaderFiles = glob.glob(os.path.join(projectPath, 'scenes', 'master', 'char', '*', 'shaders', 'shaderMan', '*.ma'))
	for shaderFile in shaderFiles:
		if os.path.exists(shaderFile):
			utils.backupFile(shaderFile, verbose=False)

	# TODO: For mentalRay, the render settings don't seem to get loaded in exportAll mode, so they can't be found and exported..
	'''
	if renderer == 'mentalRay':
		render.util.loadMR()
	elif renderer == 'vray':
		render.util.loadVR()
	'''
   
	try:
		filer.openCharacter(char)
	except:
		var = raw_input('** The character %s has no mtl file. Skipping.. Press ENTER to close this window. **' % char)

	try:
		multiMtlExport=ShaderManUI()
		multiMtlExport.exportShaders()
		var = raw_input('** The character %s was successfully exported.  Press ENTER to close this window. **' % char)
	except:
		var = raw_input('** There was an error. **\n**Check the output above. Press ENTER to close this window. **')

