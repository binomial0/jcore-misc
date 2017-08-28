
'''
Created on 25.08.2017
@author: egrygorova
'''

import os
import sys
import xml.etree.ElementTree as ElementTree

def changeDescVersion(pTree, toVersion, pName, xmlns, xmlns_URI):
    for p in pTree.iter(tag=xmlns):
        for child in p:
            for v in child:
                    if nodeHasTag(v, "version", xmlns_URI):#wenn der Tag version heisst dann den Text dort ersetzen
                        print("old value: ", v.text)
                        v.text = toVersion
                        print("new value: ", v.text)
                        pTree.write(descFile, encoding="utf-8", xml_declaration=True)
                        print("[desc File] %s changed version:\n\t to %s"
                                % (pName, toVersion))


def nodeHasTag(node, name, xlmns):#if node e.g. has tag version
    if (node.tag == xlmns + name):
        print("nodeTag: ", node.tag, " xmlns + name : ", xlmns + name)
        return True
    else:
        return False
    
def tag_uri(elem):
    if elem.tag[0] == "{":
        return elem.tag[0:42]

####################################################################################################################################    

if len(sys.argv) != 3:
    print("usage: updateDescriptor.py <parent directory> <to version> ")
    
else:
    #fromVersion = sys.argv[3]
    toVersion = sys.argv[2]
    pParentDir = os.path.abspath(sys.argv[1])

    count = 0
    gIgnore = [x.rstrip("\n") for x in open(pParentDir + os.path.sep + ".gitignore").readlines()]
    
    if (__name__ == "__main__"):
        for project in os.listdir(pParentDir):  # all projects from jcore-projects
            pPath = pParentDir + os.path.sep + project
            if (os.path.isdir(pPath) and (project not in gIgnore) and not project.endswith(".git") and not project.endswith(".settings") and not project.endswith("META-INF")):  # if project is a directory and not .gitignore
                print("Project Path: " + pPath)
                for root, dirs, files in os.walk((os.path.sep).join(
                        [pPath, "src", "main", "resources", "de", "julielab"])):
                    subDir = os.path.basename(os.path.normpath(root))
                    print("subDir: " + subDir)
                    if subDir == 'desc':
                        for filename in files:
                            descFile = root + os.path.sep + filename
                            print("descFile: " + descFile)
                            ElementTree.register_namespace("", "http://uima.apache.org/resourceSpecifier")
                            tree = ElementTree.parse(descFile)
                            xmlns = tree.getroot()
                            #print("xmlns: ", xmlns)
                            xmlnsTag = xmlns.tag
                            #print("xmlnsTag : ", xmlnsTag)
                            xmlns_URI = tag_uri(xmlns)
                            #print("Tag URI: " , xmlns_URI)
                            changeDescVersion(tree, toVersion, descFile, xmlnsTag, xmlns_URI)
                print("#######################################################################################################")
