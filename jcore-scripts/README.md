## updatePomVersion.py
Since the maven-release-plugin wouldn't do what we needed for changing version numbers, there is a Python script that goes through all projects in a parent folder and
* changes the version of the `parent pom` to the one specified
* removes the version number of the module if it's present (all modules shall inherit the `parent pom`s version
* changes any `jcore` dependency version numbers to `${jcore-version}`
The script can be improved in some aspects, but right now if you can execute it with
```
python updatePomVersion.py PATH_TO_PARENT_PROJECT_FOLDER TO_VERSION FROM_VERSION
```
For instance to update all modules of `jcore-base` that is located in `/home/git/jcore-base` from version `2.0.0` to `2.1.0-SNAPSHOT` call
```
python updatePomVersion.py /home/git/jcore-base 2.1.0-SNAPSHOT 2.0.0
```
The script is not compatible with python version < 3.

## updateUIMAVersions.py
This script updates the version tags in UIMA Descriptor files.  
It takes two arguments: the new version and the directory in which to look for UIMA Descriptors.

It sometimes reformats the code a little bit (for example, <tag/> becomes <tag />)
