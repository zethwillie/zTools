import sys

syspaths = sys.path

for path in syspaths:
	print path

# have to split these before printing out. make an interface
# scriptPaths = mel.getenv("MAYA_SCRIPT_PATH")
# plugInPaths = mel.getenv("MAYA_PLUG_IN_PATH")
# pythonPaths = mel.getenv("PYTHONPATH")
# iconPaths = mel.getenv("XBMLANGPATH")
# pathPaths = mel.getenv("PATH")