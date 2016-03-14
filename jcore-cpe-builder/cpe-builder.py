# -*- coding: utf-8 -*-

DESC_NAME = "SOME-DESC-NAME"
NAME_VALUE_PAIR = "SOME-NAME-VALUE-PAIR"
NAME = "SOME-NAME"
TYPE = "SOME-TYPE"
VALUE = "SOME-VALUE"
CAS_PROC = "SOME-CAS-PROCESSOR"
CONFIG_PARAMS = "SOME-CONFIG-PARAM"

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


testDesc = "de.julielab.jcore.reader.file.desc.jcore-file-reader"
testValueName = "InputDirectory"
testValueType = "string"
testValue = "data/inFiles"

cr = buildCollectionReader(testDesc,
        buildConfigParams(
            buildNameValue(testValueName,
                buildValue(testValueType, testValue)
                )
            )
        )

print(buildCASProcs([1,2]))