import fileinput
import re
import os
import sys

#function which replaces the license header
def replaceHeader(path, licenseFile):
 #delete the header until package
 foundPackage = False;

 for line in fileinput.input(path, inplace=True):
	 if re.match("package", line):
		 foundPackage = True
	 if foundPackage:
		 print(line, end="")
	 else:
		 print(end="")
 #insert content from LICENSE FILE at the beginning
 with open(licenseFile, "r") as licFile:
	 licRead = licFile.readlines()
 with open(path, "r") as newFile:
	 newRead = newFile.readlines()
 newRead.insert(0, licRead)
 with open(path, "w") as newFile:
		for item in newRead:
	 		 newFile.writelines(item)

##########################################################################

if len(sys.argv) != 3:
	print("usage: replaceHeader.py <path to directory> <path to license file>")

else: 
 srcDir = str(sys.argv[1])
 licenseFile = str(sys.argv[2])
#walk recursively through source Directory
 for dirpath, dirs, files in os.walk(srcDir):	
	 for filename in files:
		 path = os.path.join(dirpath,filename)
		 if "/de/julielab" in path:
			 if filename.endswith(".java"):
				 #print("Replaced Header in File: " + path)
				 replaceHeader(path, licenseFile)
		 else:
			 if filename.endswith(".java"):
				 print("WARNING: NOT A /de/julielab DIRECTORY! " + path)
