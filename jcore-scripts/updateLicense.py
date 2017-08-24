import fileinput
import re
import os
import sys


#function which replaces the line in the license header
def replaceHeader(path):
	with fileinput.FileInput(path, inplace=True) as newFile:
		for line in newFile:
			print(line.replace("GNU Lesser General Public License (LGPL) v3.0", "BSD-2-Clause License"), end = "")
 
#function which replaces whole license text in the LICENSE files
def replaceLicenseText(path, newLicenseFile):
	with open(newLicenseFile, "r") as licFile:
		licRead = licFile.readlines()
	with open(path, "w") as newFile:
		for item in licRead:
			newFile.write(item)


#####################################################################################################################

if len(sys.argv) != 3:
	print("usage: updateLicense.py <path to directory> <path to license file>")

else: 
 srcDir = str(sys.argv[1]) # source directory
 newLicenseFile = str(sys.argv[2]) # path to the file with the new license content
#walk recursively through source Directory
 for dirpath, dirs, files in os.walk(srcDir):	
	 for filename in files:
		 basicpath = os.path
		 path = os.path.join(dirpath,filename)
		 if filename.startswith("LICENSE") and "/target" not in path:
			 replaceLicenseText(path, newLicenseFile)
			 print("Replaced old Content in License File in :" + path)
		 if "/de/julielab" in path:
			 if filename.endswith(".java"):
				 print("Replaced Header in File: " + path)
				 replaceHeader(path)
		 else:
			 if filename.endswith(".java"):
				 print("WARNING: NOT A /de/julielab DIRECTORY! " + path)
