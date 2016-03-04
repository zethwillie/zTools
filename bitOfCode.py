import maya.utils as utils

utils.executeDeferred("CodeHere")

#I can also import in a userSetup.py, maya.cmds and have it be there in my session without having to keep calling it

import sys

sys.path.split("path goes here")
sys.path.join("path goes here") #these two will create/get rid of the correct path separators ("/" or "\") automagically

# look in maya.utils. . . 

