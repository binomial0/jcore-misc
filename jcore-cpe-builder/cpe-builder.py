# -*- coding: utf-8 -*-

import json
import os
import sys

DEBUG = False
WS = '\t'

### HEADER ###
HEAD = (
"""<?xml version="1.0" encoding="UTF-8"?>\n""" +
"""<cpeDescription xmlns="http://uima.apache.org/resourceSpecifier">\n"""
)


### END ###
END = (
"""<cpeConfig>\n""" +
"""\t<numToProcess>-1</numToProcess>\n""" +
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


def buildConfigParams(cp_dict,tab=1):
    cp_string = ""
    cp_param_list = []
    for i in ["mandatory", "optional"]:
        cp_param_list.extend(cp_dict[i])
    for param in cp_param_list:
        nv_pair = buildNameValue(param["name"],
            buildValue(param["type"], param["default"]), tab + 1)
        cp_string += nv_pair
    cp_string = cp_string.rstrip('\n')

    CONFIG_PARAMS = (
    """{}<configurationParameterSettings>\n""" +
    """{}\n""" +
    """{}</configurationParameterSettings>"""
    ).format(tab * WS, cp_string, tab * WS)

    return CONFIG_PARAMS


def buildCollectionReader(cr_dict):
    # e.g. cDescName=de.julielab.jcore.reader.file.desc.jcore-file-reader
    crDescName = cr_dict["desc"]
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


def buildCASProcs(casProcs):
    procs = ""
    if isinstance(casProcs, list):
        for proc in casProcs:
            name = ", ".join([proc["name"], proc["model"]])
            cp = buildConfigParams(proc, 3)
            procs += buildCASProc(name, proc["desc"], cp)
        procs = procs.rstrip("\n")
    else:
        pass
    CAS_PROCS = (
    """\t<casProcessors casPoolSize="3" processingUnitThreadCount="1">\n""" +
    """{}\n""" +
    """\t</casProcessors>\n""").format(procs)

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

    # write out
    print(cr_string+ae_string)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "true":
            DEBUG = True

    modifyPipeline()
    print("\nbuild pipeline ...")
    buildCurrentPipeline()