#!/bin/bash
# This script uses the JULIE XML tools to extract the parameters from UIMA
# component descriptors and then arranges them to form a markdown
# table to use in GitHub README.md files.

echo "| Parameter Name | Parameter Type | Mandatory | Multivalued | Description |"
echo "|----------------|----------------|-----------|-------------|-------------|"
java -cp resources/julie-xml-tools.jar de.julielab.xml.JulieXMLToolsCLIRecords $1 //configurationParameter name type mandatory multiValued description | sed 's/	/ | /g;s/^/| /;s/$/ |/'

