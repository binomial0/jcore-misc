#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script created the component.meta files for all projects in some jcore repository.
I.e. to create the meta information for jcore-base, point the script at the
jcore-base directory. It will automatically create the component.meta file for
all projects in jcore-base.
"""
import os
import sys
import json
import fnmatch
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

# For testing we define in and out names so we can create new versions and compare
META_DESC_IN_NAME = "component.meta"
META_DESC_OUT_NAME = "component.meta"

def getNodeText(nodelist):
	"""
	Meant to be used with nodelists that have zero or one elements.
	Returns the text content of the first element, if it exists.
	"""
	if len(nodelist) > 0:
		return nodelist[0].text
	return ""

def getArtifactInfo(pomFile):
		# POMs have a default namespace. We define it here for
		# the "d"(efault) prefix (the name is arbitrary) and
		# use it to provide the namespaces for XPath expressions
		ns = {"d":"http://maven.apache.org/POM/4.0.0"}
		root = ET.parse(pomFile)
		nameNodes = root.findall("./d:name", ns)
		descriptionNodes = root.findall("./d:description", ns)
		artifactIdNodes = root.findall("./d:artifactId", ns)

		name = ""
		description = ""
		artifactId = ""
		name = getNodeText(nameNodes)
		description = getNodeText(descriptionNodes)
		artifactId = getNodeText(artifactIdNodes)
		category = None
		if (artifactId.endswith("reader")):
			category = "reader"
		if (artifactId.endswith("ae")):
			category = "ae"
		if (artifactId.endswith("multiplier")):
			category = "multiplier"
		if (artifactId.endswith("consumer")):
			category = "consumer"
		if (artifactId.endswith("writer")):
			category = "consumer"

		return artifactId, name, category, description

def getDescriptors(projectpath):
	"""
	This method returns all XML files that
	1. Are located in the JCoRe-conventional descriptor directory
	2. Look like a UIMA component descriptor on a quick glance
	"""
	ns = {"d":"http://uima.apache.org/resourceSpecifier"}
	descriptors = []
	for root, dirnames, filenames in os.walk(projectpath + os.path.sep + os.path.sep.join(["src", "main", "resources", "de", "julielab", "jcore"])):
		if (root.endswith("desc")):
			for filename in fnmatch.filter(filenames, '*.xml'):
				tree = None
				try:
					tree = ET.parse(root + os.path.sep + filename)
				except ParseError as e:
					print ("Could not parse file {}: {}".format(root + os.path.sep + filename, e))
				descriptorRoot = tree.getroot()
				outputsNewCASes = False
				outputsCasesNodes = descriptorRoot.findall(".//d:outputsNewCASes", ns)
				if len(outputsCasesNodes) > 0 and outputsCasesNodes[0].text.lower() == "true":
					outputsNewCASes = True
				category = None
				if descriptorRoot.tag.endswith("collectionReaderDescription"):
					category = "reader"
				if descriptorRoot.tag.endswith("analysisEngineDescription"):
					category = "ae"
					if outputsNewCASes:
						category = "multiplier"
				if descriptorRoot.tag.endswith("casConsumerDescription"):
					category = "consumer"
				if category != None:
					# From the complete file name, exclude the system dependent part. That is, make the path relative to the
					# project directory's src/main/resources directory.
					location = os.path.join(root, filename)[len(projectpath+os.path.sep+os.path.sep.join(["src", "main", "resources"]))+1:]
					# And then make it to be a lookup by name: Use a dot as the path separator and remove the file name extension
					location = location.replace(os.path.sep, ".")
					# Remove '.xml'
					location = location[:-4]
					descriptors.append({"location":location,"category":category})
	return descriptors

def mergeWithOldMeta(projectPath, description):
	"""
	Reads potentially existing meta descriptor information
	and extracts information from it that can't be automatically
	derived from the POM and the descriptors.
	This is currently the group in which the component
	is manually inserted and the exposable attribute.
	"""
	metaDescFileName = projectPath + os.path.sep + META_DESC_IN_NAME
	group = "general"
	exposable = description["descriptors"] != None and len(description["descriptors"]) > 0;
	if os.path.exists(metaDescFileName):
		with open(metaDescFileName, 'r') as metaDescFile:
			oldDescription = json.load(metaDescFile)
			group = oldDescription["group"]
			#exposable = oldDescription["exposable"]
	description["group"] = group
	description["exposable"] = exposable


if (__name__ == "__main__"):
	if len(sys.argv) > 1:
		pParentDir = sys.argv[1]
		print ("Creating or updating {} files in repository {}".format(META_DESC_OUT_NAME, pParentDir))
		numCreated = 0
		for project in os.listdir(pParentDir):
			pPath = pParentDir+project
			pomFile = pPath + os.path.sep + "pom.xml"

			if os.path.exists(pomFile):
				artifactId, name, category, description = getArtifactInfo(pomFile)
				if category != None:
					description = {
					 "name":name,
					 "maven-artifact":artifactId,
					 "description": description,
					 "category":category
					}
					description["descriptors"] = getDescriptors(pPath)
					mergeWithOldMeta(pPath, description)
					jsonDesc = json.dumps(description, sort_keys=True, indent=4, separators=(",", ": ")) + os.linesep
					with open(pPath + os.path.sep + META_DESC_OUT_NAME, 'w') as metaDescFile:
						metaDescFile.write(jsonDesc)
					numCreated = numCreated + 1
		print ("Created or updated {} {} files in {}.".format(numCreated, META_DESC_OUT_NAME, pParentDir))
	else:
		print ("You need to pass the local JCoRe repository location as parameter.")

