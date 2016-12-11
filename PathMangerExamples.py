from chrlx.utils import PathManager

path = PathManager("G:\jobs\charlex_testArea_T60173\W_psultan\scenes\shot010\lgt\workshop\T60173W_010_std_software.01.ma")

#job info determined by folder structure
print "jobNumber:", path.jobNumber
print "jobDirname:", path.jobDirname
print "jobShortname:", path.jobShortname
print "jobType:", path.jobType
print "jobPath:", path.jobPath 
print "spotLetter:", path.spotLetter 
print "spotDirname:", path.spotDirname 
print "spotFullname:", path.spotFullname 
print "spotShortname:", path.spotShortname 
print "spotSchema:", path.spotSchema 
print "spotPath:", path.spotPath 
print "projectPath:", path.projectPath 
print "configPath:", path.configPath 
print "assetPath:", path.assetPath 
print "charPath:", path.charPath 
print "propPath:", path.propPath 
print "shot:", path.shot 
print "shotName:", path.shotName 
print "shotType:", path.shotType 
print "shotFullname:", path.shotFullname 
print "shotShortname:", path.shotShortname 
print "shotStage:", path.shotStage 
print "scenePath:", path.scenePath 
print "compPath:", path.compPath 
print "anmPath:", path.anmPath 
print "lgtPath:", path.lgtPath 
print "jobId", path.job.id       #many attributes are accessible with dot notation

#folder navigation
print "scenePath", path.scenePath
print "compPath", path.compPath
print "framesPath", path.framesPath

#job info determined by db
print "start_date", path.job.start_date
print "status", path.spot.status

#lgt shot specific functions
print "variants", path.getVariants()
print "masters", path.getMasters()
print "mastername", path.getMasterName()
print "version", path.getVersion()
