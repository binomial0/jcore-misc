'''
Created on 25.08.2017

@author: egrygorova
'''
import os
import sys
import xml.etree.ElementTree as ElementTree

def changeParentVersion(pTree, toVersion, fromVersion, pName, xmlns, xmlns_URI):
    for p in pTree.iter(tag=xmlns):
        for child in p:
            for v in child:
                    if nodeHasTag(v, "version", xmlns_URI):#wenn der Tag version heißt dann den Text dort ersetzen
                        print("alter Text: ", v.text)
                        if (fromVersion == v.text):#TODO egal welche Version da steht, immer durch 2.3.0 ersetzen?
                            v.text = toVersion
                            print("Neuer Text: ", v.text)
                            print("[parent POM] %s changed version:\n\t from %s to %s"
                                % (pName, fromVersion, toVersion))
                        else:
                            print("[ERROR] %s parent POM version is:\n\t %s but argument input said it should be %s."
                                % (pName, v.text, fromVersion))


def nodeHasTag(node, name, xlmns):
    #print("nodeTag: ", node.tag, " xmlns + name : ", xlmns + name)
    if (node.tag == xlmns + name):
        return True
    else:
        #print("FALSE!")
        return False
    
def tag_uri(elem):
    if elem.tag[0] == "{":
        return elem.tag[0:42]
####################################################################################################################################    
if len(sys.argv) != 4:
    print("usage: updateDescriptor.py <parent directory> <to version> <from version> ")
    
else:
    fromVersion = sys.argv[3]
    toVersion = sys.argv[2]
    pParentDir = os.path.abspath(sys.argv[1])

    count = 0
    gIgnore = [x.rstrip("\n") for x in open(pParentDir + os.path.sep + ".gitignore").readlines()]
    # for item in gIgnore:
        # print("gitignore: " + item)
    
    if (__name__ == "__main__"):
        for project in os.listdir(pParentDir):  # all projects from jcore-projects
            pPath = pParentDir + os.path.sep + project
            if (os.path.isdir(pPath) and (project not in gIgnore) and not project.endswith(".git") and not project.endswith(".settings") and not project.endswith("META-INF")):  # if project is a directory and not .gitignore
                print("Project Path: " + pPath)
                for root, dirs, files in os.walk((os.path.sep).join(
                        [pPath, "src", "main", "resources", "de", "julielab"])):
                    foo = os.path.basename(os.path.normpath(root))
                    # print("FOO: " + foo)
                    if foo == 'desc':
                        for filename in files:
                            descFile = root + os.path.sep + filename
                            # print("Root: " + root)
                            print("Der Pfad: " + descFile)
                            tree = ElementTree.parse(descFile)
                            xmlns = tree.getroot()
                            print("xmlns: ", xmlns)
                            xmlnsTag = xmlns.tag
                            print("xmlnsTag : ", xmlnsTag)
                            xmlns_URI = tag_uri(xmlns)
                            print("Tag URI: " , xmlns_URI)
                            changeParentVersion(tree, toVersion, fromVersion, descFile, xmlnsTag, xmlns_URI)
                print("#######################################################################################################")
