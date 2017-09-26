import fileinput
import re
import os
import sys

#function which replaces the line in the license header
def replaceLineInHeader(path):
	with fileinput.FileInput(path, inplace=True) as newFile:
		for line in newFile:
			print(line.replace("GNU Lesser General Public License (LGPL) v3.0", "BSD-2-Clause License"), end = "")
	print("replaced line in license header in: " + path)

#function which adds new license header if first line is 'package'
def addNewLicenseHeader(path, licenseHeader):
 with open(licenseHeader, "r") as licFile:
	 	licRead = licFile.readlines()
 with open(path, "r") as newFile:
	 	newRead = newFile.readlines()
 newRead.insert(0, licRead)
 with open(path, "w") as newFile:
		for item in newRead:
	 		 newFile.writelines(item)
 print("added new license header in: " + path)
	
 
#function which replaces whole license text in the LICENSE files
def replaceLicenseText(path, newLicenseFile):
	with open(newLicenseFile, "r") as licFile:
		licRead = licFile.readlines()
	with open(path, "w") as newFile:
		for item in licRead:
			newFile.write(item)

#function which gets first line of a given file
def getfirstline(path):
	with open(path, 'r') as fi:
		firstline = fi.readline()
	return firstline

if len(sys.argv) != 4:
	print("usage: updateLicense.py <path to directory> <path to license file> <path to new license header template>")

else: 
 srcDir = str(sys.argv[1]) # source directory
 newLicenseFile = str(sys.argv[2]) # path to the file with the new license content
 newLicenseHeader = str(sys.argv[3]) #path to the file with new license header
#walk recursively through source Directory
 for dirpath, dirs, files in os.walk(srcDir):	
	 for filename in files:
		 path = os.path.join(dirpath,filename)
		 if filename.startswith("LICENSE") and "/target" not in path:
			 replaceLicenseText(path, newLicenseFile)
			 print("Replaced old Content in License File in :" + path)
		 if "/de/julielab" in path and not "/jcore-types/" in path:
			 if filename.endswith(".java"):
				 newline = getfirstline(path)
				 if newline.startswith("/*"):
				 	 replaceLineInHeader(path)
				 elif newline.startswith("package"):
				 	 addNewLicenseHeader(path, newLicenseHeader)
				 else:
					 print("WARNING! NO APPROPRIATE HEADER!" + path)
		 else:
			 if filename.endswith(".java"):
				 print("WARNING: NOT A /de/julielab DIRECTORY!" + path)
