# -*- coding: utf-8 -*-

import json

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
    "cr": {},
    "ae": {},
    "cc": {}
    }

A_MAP = {
    "cr": int,
    "ae": [],
    "cc": int
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


def getComponent(component="ae"):
    c_dict = {
        "cr": "Collection Reader",
        "ae": "Analysis Engine",
        "cc": "Collection Consumer"
        }
    comp_string = ""
    comps = JCOORDS[(c_dict[component]).lower()]
    count = 0
    for i in sorted(list(comps.keys())):
        C_MAP[component][count] = i
        comp_string += "\t[{:>2}] {}\n".format(count, comps[i]["name"])
        count += 1

    cr = input(
    """Choose a(n) {} from the following list:
    {}Choice (q for quit): """.format(c_dict[component], comp_string)
    )

    return cr


def displayPipeline():
    ac = None
    while ac is None or ac.lower() not in ["r", "a", "c"]:
        ac = input(("""The current pipeline consists of\n""" +
                    """Collection Reader:\n\t{}""" +
                    """Analysis Engine(s):\n\t{}""" +
                    """Collection Consumer:\n\t{}""" +
                    """modify (r)eader, (a)nalysis engines or (c)onsumers: """
                    ).format("aa\n",
                             "bb\n",
                             "cc\n")
                    )

    return ac

if __name__ == "__main__":
    #getComponent()
    displayPipeline()