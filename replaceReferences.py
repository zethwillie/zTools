"""for switching out references when you dupe a character"""

import fileinput

#just get file that we've previously reffed
#then get the place where the file will be now
prevRef = "//Bluearc/GFX/jobs/verizonFios_P12929/C_gatewayRouter//scenes/master/char/rocks/geo/rocks.ma"
newRef = "//Bluearc/HOME/CHRLX/zwillie/Windows/Desktop/pageRig.ma"

for line in fileinput.FileInput("//Bluearc/HOME/CHRLX/zwillie/Windows/Desktop/testingREF.ma",inplace=1):
    line = line.replace(prevRef,newRef)
    print line