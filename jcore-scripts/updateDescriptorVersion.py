# -*- coding: utf-8 -*-
import os
import sys
from xml.etree.ElementTree import ElementTree

fromVersion = sys.argv[3]
toVersion = sys.argv[2]
pParentDir = os.path.abspath(sys.argv[1])

count = 0
gIgnore = [x.rstrip("\n") for x in open(pParentDir+os.path.sep+".gitignore").readlines()]

def changeParentVersion(pTree, toVersion, fromVersion, pName, xlmns):
    for p in pTree.iter(tag=xlmns+"project"):
        for child in p:
            if nodeHasTag(child,"parent",xlmns):
                for v in child:
                    if nodeHasTag(v,"version",xlmns):
                        if (fromVersion == v.text):
                            v.text = toVersion
                            print("[parent POM] %s changed version:\n\t from %s to %s"
                                %(pName, fromVersion, toVersion))
                        else:
                            print("[ERROR] %s parent POM version is:\n\t %s but argument input said it should be %s."
                                %(pName, v.text, fromVersion))

def deleteSelfVersion(pTree, pName, xlmns):
    for p in pTree.iter(tag=xlmns+"project"):
        for child in p:
            if nodeHasTag(child,"version",xlmns):
                p.remove(child)
                print("[self version] %s: removed individual version." %(pName))

def changeDependenciesVersion(pTree, pName, xlmns):
    for p in pTree.iter(tag=xlmns+"project"):
        for child in p:
            if nodeHasTag(child,"dependencies",xlmns):
                for dep in child:
                    for v in dep:
                        if nodeHasTag(v,"artifactId",xlmns):
                            dName = v.text
                        if nodeHasTag(v,"version",xlmns):
                            nText = "${jcore-version}"
                            if (dName.split("-")[0] == "jcore"):
                                if (v.text != nText):
                                    print("[dependencies version] %s:\n\t changed %s version: %s -> %s"
                                        %(pName, dName, v.text, nText))
                                    v.text = nText

def nodeHasTag(node, name, xlmns):
    if (node.tag == xlmns+name):
        return True
    else:
        return False

if (__name__ == "__main__"):
    for project in os.listdir(pParentDir):
        pPath = pParentDir+os.path.sep+project
        if (os.path.isdir(pPath) and (project not in gIgnore)):
            for root, dirs, files in os.walk((os.path.sep).join(
                    [pPath,"src","main","resources","de","julielab"])):
                foo = os.path.basename(os.path.normpath(root))
                if foo == 'desc':
                    for fi in files:
                        descFile = root+os.path.sep+fi
                #pomFile = pPath+os.path.sep+"pom.xml"
                #if (os.path.exists(pomFile)):
                    #tree = ElementTree()
                    #tree.parse(pomFile)
                    #root = tree.getroot()
                    #xlmns = (root.tag).rstrip("project")

                    #changeParentVersion(tree, toVersion, fromVersion, project, xlmns)
                    #deleteSelfVersion(tree, project, xlmns)
                    #changeDependenciesVersion(tree, project, xlmns)

                    #tree.write(pomFile,encoding="UTF-8",xml_declaration=True,
                                        #default_namespace=xlmns[1:-1])
