# -*- coding: utf-8 -*-

import json
import os
import sys
import subprocess
import shutil
import time

DEBUG = False
WS = '\t'
TYPE_PRE = "de.julielab.jcore.types."
PIPENAME = ""
DEP_LIST = []
DIR_LIST = []

### HEADER ###
HEAD = (
"""<?xml version="1.0" encoding="UTF-8"?>\n""" +
"""<cpeDescription xmlns="http://uima.apache.org/resourceSpecifier">\n"""
)


### END ###
END = (
"""\t<cpeConfig>\n""" +
"""\t\t<numToProcess>-1</numToProcess>\n""" +
"""\t\t<deployAs>immediate</deployAs>\n""" +
"""\t\t<checkpoint batch="0" time="300000ms"/>\n""" +
"""\t\t<timerImpl/>\n""" +
"""\t</cpeConfig>\n""" +
"""</cpeDescription>\n"""
)


### PROJECTS COORDINATES ###
JCOORDS = None
with open('coordinates.json') as jfile:
    JCOORDS = json.load(jfile)
 # add short names (derived from key names) to components
for component in list(JCOORDS.keys()):
    if component != "jcore version":
        for short in list(JCOORDS[component]):
            JCOORDS[component][short]["short"] = short

C_MAP = {
    "cr": {"None": "None"},
    "ae": {"None": "None"},
    "cc": {"None": "None"}
    }

A_MAP = {
    "cr": "None",
    "ae": ["None"],
    "cc": "None"
    }


### BUILDING FUNCTIONS ###
def buildValue(vType, vValue):
    # e.g. <string>data/inFiles</string>
    VALUE = (
    """<{}>{}</{}>"""
    ).format(vType, vValue, vType)

    return VALUE


def buildNameValue(nvName, nvValue, tab=1):
    # e.g. NAME = InputDirectory
    NAME_VALUE_PAIR = (
    """{}<nameValuePair>\n""" +
    """{}\t<name>{}</name>\n""" +
    """{}\t<value>\n""" +
    """{}\t\t{}\n""" +
    """{}\t</value>\n""" +
    """{}</nameValuePair>\n"""
    ).format(tab * WS, tab * WS,
             nvName, tab * WS, tab * WS,
             nvValue, tab * WS, tab * WS)

    return NAME_VALUE_PAIR


def buildConfigParams(cp_dict, tab=1):
    global DIR_LIST
    cp_string = ""
    cp_param_list = []
    for i in ["mandatory", "optional"]:
        cp_param_list.extend(cp_dict[i])
    for param in cp_param_list:
        nv_pair = buildNameValue(param["name"],
            buildValue(param["type"], param["default"]), tab + 1)
        if param.get("dir", False):
            DIR_LIST.append(param["default"])
        cp_string += nv_pair
    cp_string = cp_string.rstrip('\n')

    CONFIG_PARAMS = (
    """{}<configurationParameterSettings>\n""" +
    """{}\n""" +
    """{}</configurationParameterSettings>"""
    ).format(tab * WS, cp_string, tab * WS)

    return CONFIG_PARAMS


def buildCollectionReader(cr_dict):
    global DEP_LIST
    # e.g. cDescName=de.julielab.jcore.reader.file.desc.jcore-file-reader
    crDescName = cr_dict["desc"]
    DEP_LIST.append(crDescName.split('.')[-1])
    crConfigParams = buildConfigParams(cr_dict, 3)

    CR = (
    """\t<collectionReader>\n""" +
    """\t\t<collectionIterator>\n""" +
    """\t\t\t<descriptor>\n""" +
    """\t\t\t\t<import name="{}"/>\n""" +
    """\t\t\t</descriptor>\n""" +
    """{}\n""" +
    """\t\t</collectionIterator>\n""" +
    """\t</collectionReader>\n""").format(crDescName, crConfigParams)

    return CR


def buildCASProcs(casProcs, is_ae=True):
    global PIPENAME
    global DEP_LIST
    procs = ""
    if isinstance(casProcs, list):
        PIPENAME = casProcs[-1]["short"]
        for proc in casProcs:
            cpDescName = proc["desc"]
            name = ", ".join([proc["name"], proc["model"]])
            cp = buildConfigParams(proc, 3)
            procs += buildCASProc(name, cpDescName, cp)
            DEP_LIST.append(cpDescName.split('.')[-1])
        procs = procs.rstrip("\n")
    else:
        cp = buildConfigParams(casProcs, 3)
        cpDescName = casProcs["desc"]
        procs = buildCASProc(casProcs["name"], cpDescName, cp)
        DEP_LIST.append(cpDescName.split('.')[-1])
        procs = procs.rstrip("\n")
    CAS_PROCS = ""
    if is_ae:
        CAS_PROCS =\
        """\t<casProcessors casPoolSize="3" processingUnitThreadCount="1">\n"""
    CAS_PROCS += ("""{}\n""").format(procs)
    if not is_ae:
        CAS_PROCS += """\t</casProcessors>\n"""

    return CAS_PROCS


def buildCASProc(casName, casDescName, casCP):
    ### SINGLE CAS PROCESSOR ###
    CAS_PROC = (
    """\t\t<casProcessor deployment="integrated" name="{}">\n""" +
    """\t\t\t<descriptor>\n""" +
    """\t\t\t\t<import name="{}"/>\n""" +
    """\t\t\t</descriptor>\n""" +
    """{}\n""" +
    """\t\t\t<deploymentParameters/>\n""" +
    """\t\t\t<errorHandling>\n""" +
    """\t\t\t\t<errorRateThreshold action="terminate" value="0/1000"/>\n""" +
    """\t\t\t\t<maxConsecutiveRestarts action="terminate" value="30"/>\n""" +
    """\t\t\t\t<timeout max="100000" default="-1"/>\n""" +
    """\t\t\t</errorHandling>\n""" +
    """\t\t\t<checkpoint batch="10000" time="1000ms"/>\n""" +
    """\t\t</casProcessor>\n""").format(casName, casDescName, casCP)

    return CAS_PROC


def quitSystem():
    if DEBUG:
        print("\n[DEBUG] Map of Components:")
        print(A_MAP)
    sys.exit()


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def removeLastComponent(component):
    if component == "ae":
        tmp = A_MAP[component].pop()
        if (tmp is "None") or (len(A_MAP[component]) == 0):
            A_MAP[component].append("None")
    else:
        A_MAP[component] = "None"


def getCompName(component, index):
    c_dict = {
        "cr": "Collection Reader",
        "ae": "Analysis Engine",
        "cc": "CAS Consumer"
        }
    name = "None"
    jShort = C_MAP[component][index]
    if jShort != "None":
        name = JCOORDS[(c_dict[component]).lower()][jShort]["name"]

    return name


def getComponent(component="ae"):
    c_dict = {
        "cr": "Collection Reader",
        "ae": "Analysis Engine",
        "cc": "CAS Consumer"
        }
    comp_string = ""
    comps = JCOORDS[(c_dict[component]).lower()]
    count = 0
    for i in sorted(list(comps.keys())):
        C_MAP[component][str(count)] = i
        comp_string += "\t[{:>2}] {}\n".format(count, comps[i]["name"])
        count += 1

    cr = None
    choice = """Choose a {} from the following list:"""
    if component == "ae":
        choice = """Add an {} from the following list:"""

    while cr is None or cr not in ["q", "p"]:
        displayPipeline()
        cr = input(
        (choice +
         """\n{}\nChoice (p for 'back to previous'; q for 'quit'; """ +
         """r for 'remove last'): """)
        .format(c_dict[component], comp_string)
        )
        cr = cr.lower()
        if cr in [str(x) for x in range(len(C_MAP[component]) - 1)]:
            if component == "ae":
                if "None" in A_MAP[component]:
                    A_MAP[component].remove("None")
                A_MAP[component].append(cr)
            else:
                A_MAP[component] = cr

        if cr == "r":
            removeLastComponent(component)

    if cr == "q":
        quitSystem()
    elif cr == "p":
        modifyPipeline()


def displayPipeline():
    clearScreen()
    print(("""The current pipeline consists of\n""" +
           """Collection Reader:\n\t{}""" +
           """Analysis Engine(s):\n\t{}""" +
           """Collection Consumer:\n\t{}"""
           ).format(getCompName("cr", A_MAP["cr"]) + "\n",
                ", ".join([getCompName("ae", x) for x in A_MAP["ae"]]) + "\n",
                getCompName("cc", A_MAP["cc"]) + "\n")
           )


def modifyPipeline():
    ac = None
    while ac is None or ac not in ["r", "a", "c", "q", "n"]:
        displayPipeline()
        ac = input("""modify (r)eader, (a)nalysis engines or (c)onsumer\n""" +
                    """(n for 'build current pipeline'; q for 'quit'): """)
        ac = ac.lower()

    if ac == "q":
        quitSystem()
    elif ac == "r":
        getComponent("cr")
    elif ac == "c":
        getComponent("cc")
    elif ac == "n":
        if DEBUG:
            print("\n[DEBUG] Map of Components:")
            print(A_MAP)
        pass
    else:
        getComponent()


def writePom():
    print("write POM...")
    sys.stdout.flush()
    time.sleep(0.5)

    dependencies = ""
    for dep in DEP_LIST:
        dependencies += (
        """\t\t<dependency>\n""" +
        """\t\t\t<groupId>de.julielab</groupId>\n""" +
        """\t\t\t<artifactId>{}</artifactId>\n""" +
        """\t\t\t<version>${{jcore-version}}</version>\n""" +
        """\t\t</dependency>\n"""
        ).format(dep)
    dependencies = dependencies.rstrip("\n")

    out_string = (
        """<?xml version='1.0' encoding='UTF-8'?>\n""" +
        """<project xmlns="http://maven.apache.org/POM/4.0.0" """ +
        """xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" """ +
        """xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 """ +
        """http://maven.apache.org/xsd/maven-4.0.0.xsd">\n""" +
        """\t<modelVersion>4.0.0</modelVersion>\n""" +
        """\t<parent>\n""" +
        """\t\t<groupId>de.julielab</groupId>\n""" +
        """\t\t<artifactId>jcore-pipelines</artifactId>\n""" +
        """\t\t<version>{}</version>\n""" +
        """\t</parent>\n""" +
        """\t<artifactId>{}</artifactId>\n""" +
        """\t<name>{}</name>\n""" +
        """\t<dependencies>\n""" +
        """{}\n""" +
        """\t</dependencies>\n""" +
        """</project>"""
        ).format(JCOORDS["jcore version"], PIPENAME + "-pipeline",
                 JCOORDS["analysis engine"][PIPENAME]["name"] + " Pipeline",
                 dependencies)
    with open("pom.xml", 'w') as out_file:
        out_file.write(out_string)


def copyInstallScript():
    iScript = os.path.abspath("../installComponents_template")
    shutil.copy(iScript, "installComponents.sh")

    subprocess.call(
    ["chmod", "+x", "installComponents.sh"]
    )


def writeExecutionScript(cpeName):
    print("create Scripts...")
    sys.stdout.flush()
    time.sleep(0.5)

    xScript = (
    """#!/bin/bash\n\n""" +
    """java_libs=target/dependency\n\n""" +
    """export CLASSPATH=`for i in $java_libs/*.jar; """ +
    """do echo -n "$i:";done;echo -n ""`\n\n""" +
    """$UIMA_HOME/bin/runCPE.sh {}""").format(cpeName)

    with open("runPipeline.sh", 'w') as out_file:
        out_file.write(xScript)

    subprocess.call(
        ["chmod", "+x", "runPipeline.sh"]
        )


def createDirs():
    print("create Directories...")
    sys.stdout.flush()
    time.sleep(0.5)
    for iDir in DIR_LIST:
        if not os.path.exists(iDir):
            os.makedirs(iDir)


def buildCurrentPipeline():
    # COLLECTION READER
    cr = None
    cr_key = C_MAP["cr"][A_MAP["cr"]]
    cr_string = ""
    if cr_key.lower() != "none":
        cr = JCOORDS["collection reader"][cr_key]
        cr_string = buildCollectionReader(cr)

    # ANALYSIS ENGINES
    ae_string = ""
    ae_list = []
    for ae_key in A_MAP["ae"]:
        ae_key = C_MAP["ae"][ae_key]
        ae = None
        if ae_key.lower() != "none":
            ae = JCOORDS["analysis engine"][ae_key]
            ae_list.append(ae)
    if len(ae_list) != 0:
        ae_string = buildCASProcs(ae_list)

    # CAS CONSUMERS
    cc = None
    cc_key = C_MAP["cc"][A_MAP["cc"]]
    cc_string = ""
    if cc_key.lower() != "none":
        cc = JCOORDS["cas consumer"][cc_key]
        cc_string = buildCASProcs(cc, False)

    if DEBUG:
        print("[DEBUG] List of Dependencies:\n{}".format(DEP_LIST))

    # write out
    foo = "jcore-{}-pipeline".format(PIPENAME)
    if not os.path.exists(foo):
        os.mkdir(foo)
    os.chdir(foo)
    fiName = "{}-cpe.xml".format(PIPENAME)
    out_string = HEAD + cr_string + ae_string + cc_string + END
    with open(fiName, 'w') as out_file:
        out_file.write(out_string)

    createDirs()
    writePom()
    copyInstallScript()
    writeExecutionScript(fiName)

    os.chdir("..")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "true":
            DEBUG = True

    modifyPipeline()

    print("\nbuild pipeline ...")
    sys.stdout.flush()
    time.sleep(0.5)
    buildCurrentPipeline()