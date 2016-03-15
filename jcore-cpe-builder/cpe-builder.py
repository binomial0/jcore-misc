# -*- coding: utf-8 -*-

import json
import os
import sys

### HEADER ###
HEAD =\
"""<?xml version="1.0" encoding="UTF-8"?>
<cpeDescription xmlns="http://uima.apache.org/resourceSpecifier">
"""


### END ###
END =\
"""
    <cpeConfig>
        <numToProcess>-1</numToProcess>
        <deployAs>immediate</deployAs>
        <checkpoint batch="0" time="300000ms"/>
        <timerImpl/>
    </cpeConfig>
</cpeDescription>"""


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
    VALUE =\
    """<{}>{}</{}>""".format(vType, vValue, vType)

    return VALUE


def buildNameValue(nvName, nvValue):
    # e.g. NAME = InputDirectory
    NAME_VALUE_PAIR =\
    """<nameValuePair>
                        <name>{}</name>
                        <value>
                            {}
                        </value>
                    </nameValuePair>""".format(nvName, nvValue)

    return NAME_VALUE_PAIR


def buildConfigParams(cpNameValue):
    CONFIG_PARAMS =\
    """<configurationParameterSettings>
                    {}
                </configurationParameterSettings>""".format(cpNameValue)
    return CONFIG_PARAMS


def buildCollectionReader(crDescName, crConfigParams):
    # e.g. DESC_NAME=de.julielab.jcore.reader.file.desc.jcore-file-reader
    CR =\
    """        <collectionReader>
            <collectionIterator>
                <descriptor>
                    <import name="{}"/>
                </descriptor>
                {}
            </collectionIterator>
        </collectionReader>""".format(crDescName, crConfigParams)

    return CR


def buildCASProcs(casProcs):
    if isinstance(casProcs, list):
        procs = ""
        for proc in casProcs:
            procs += buildCASProc("name", "descName", "cp")
        procs = procs.rstrip("\n")
    else:
        pass
    CAS_PROCS =\
    """        <casProcessors casPoolSize="3" processingUnitThreadCount="1">
{}
        </casProcessors>""".format(procs)

    return CAS_PROCS


def buildCASProc(casName, casDescName, casCP):
    ### SINGLE CAS PROCESSOR ###
    CAS_PROC =\
    """            <casProcessor deployment="integrated" name="{}">
                <descriptor>
                    <import name="{}"/>
                </descriptor>
    {}
                <deploymentParameters/>
                <errorHandling>
                    <errorRateThreshold action="terminate" value="0/1000"/>
                    <maxConsecutiveRestarts action="terminate" value="30"/>
                    <timeout max="100000" default="-1"/>
                </errorHandling>
                <checkpoint batch="10000" time="1000ms"/>
            </casProcessor>\n""".format(casName, casDescName, casCP)

    return CAS_PROC


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

    while cr is None or cr not in ["q", "b"]:
        displayPipeline()
        cr = input(
        (choice +
         """\n{}\nChoice (b for 'back to previous'; q for 'quit'; """ +
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
        sys.exit()
    elif cr == "b":
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
    while ac is None or ac not in ["r", "a", "c", "q"]:
        displayPipeline()
        ac = input("""modify (r)eader, (a)nalysis engines or (c)onsumer """ +
                    """(q for quit): """)
        ac = ac.lower()

    if ac == "q":
        sys.exit()
    elif ac == "r":
        getComponent("cr")
    elif ac == "c":
        getComponent("cc")
    else:
        getComponent()

if __name__ == "__main__":
    #getComponent()
    modifyPipeline()