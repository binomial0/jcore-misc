
import os
import sys

import xml.etree.ElementTree as ET

new_version = sys.argv[1]

print("Trying to update to version", new_version)

path = sys.argv[2]

print('Searching in', path)


def get_xmlns(tag_name):
    parts = tag_name.split('}')
    if len(parts) > 1:
        return parts[0][1:]
    else:
        return ''


def process_directory(dirname):
    for entry in os.scandir(dirname):
        if entry.is_dir():
            process_directory(entry.path)
        elif os.path.splitext(entry.name)[1] == ".xml":
            # print(entry.path)
            try:
                tree = ET.parse(entry.path)
                root = tree.getroot()
                # print(root.tag)
                xmlns = get_xmlns(root.tag)
                # print(xmlns)
                if xmlns:
                    ET.register_namespace("", xmlns)

                modified = False

                for elem in tree.iter("{http://uima.apache.org/resourceSpecifier}version"):
                    # print(elem.text)
                    old_version = elem.text
                    elem.text = new_version
                    modified = True
                    print("changed version", old_version, "to", new_version, "in", entry.path)

                if modified:
                    tree.write(entry.path, xml_declaration=True, encoding="UTF-8")

            except Exception as e:
                print(e)


process_directory(path)
