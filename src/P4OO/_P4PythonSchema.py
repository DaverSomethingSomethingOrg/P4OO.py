######################################################################
#  Copyright (c)2024 David L. Armstrong.
#
#  P4OO._P4PythonSchema.py
#
######################################################################

#NAME / DESCRIPTION
'''
Provide a set of objects that allow for interaction and translation
between P4Python output and our internally maintained Python-friendly
versions of Spec objects and Command Output.
'''

import os
import re
from datetime import datetime

import yaml
from P4OO._Exceptions import _P4OOFatal


# read in the YAML config file with our command translation table
class _P4OOP4PythonSchema():
    ''' Class to abstract the contents of our p4Config.yml file,
        separate from the execution of the p4 commands done in
        _P4Python._P4OOP4Python
    '''

    def __init__(self, configFile=None):
        self.configFile = configFile
        if self.configFile is None:
            self.configFile = os.path.dirname(__file__) + "/p4Config.yml"

        self.schemaCommands = self.readSchema(self.configFile)

    def readSchema(self, configFile):
        ''' Read in our YAML p4Config.yml file and return a dict of
            supported commands as _P4OOP4PythonCommand objects
        '''

        with open(configFile, 'r', encoding="utf-8" ) as stream:
            data = yaml.load(stream, Loader=yaml.Loader)

        return {command: _P4OOP4PythonCommand(command=command, commandDict=commandDict) for (command, commandDict) in data["COMMANDS"].items()}


    def getCmd(self, cmdName):

        if cmdName in self.schemaCommands:
            return self.schemaCommands[cmdName]

        raise _P4OOFatal("Unsupported Command " + cmdName)


    def getSpecCmd(self, specType):

        cmdObj = self.getCmd(specType)

        if cmdObj.isSpecCommand():
            return self.schemaCommands[specType]

        raise _P4OOFatal("Unsupported Spec type %s" % specType)


class _P4OOP4PythonCommand():

    def __init__(self, command=None, commandDict=None):
        self.command = command
        self.commandDict = commandDict


    def isSpecCommand(self):
        if 'specCmd' in self.commandDict:
            return True

        return False


    def isForceable(self):
        if 'forceOption' in self.commandDict:
            return True

        return False


    def isIdRequired(self):

        return self.commandDict['idRequired']


    def getSpecCmd(self):

        if self.isSpecCommand():
            return self.commandDict['specCmd']

        raise _P4OOFatal("Unsupported Spec type %s" % self.command)


    def getAllowedFilters(self):
        if 'queryOptions' in self.commandDict:
            return self.commandDict['queryOptions']

        return None


    def getAllowedConfigs(self):
        if 'configOptions' in self.commandDict:
            return self.commandDict['configOptions']

        return None


    def getOutputType(self):
        if 'output' in self.commandDict and 'p4ooType' in self.commandDict['output']:
            return self.commandDict['output']['p4ooType']

        return None


    def getOutputIdAttr(self):
        if 'output' in self.commandDict and 'idAttr' in self.commandDict['output']:
            return self.commandDict['output']['idAttr']

        return None


    def getPyIdAttribute(self):

        if self.isSpecCommand():
            return self.commandDict['idAttr']

        raise _P4OOFatal("Unsupported Spec type %s" % self.command)


    def getP4IdAttribute(self):

        pyIdAttr = self.getPyIdAttribute()

        return self.commandDict['specAttrs'][pyIdAttr]


    def translateP4SpecToPython(self, p4OutputSpec):
        ''' Translate a P4Python provided dictionary into something more
            Python-friendly.

            P4Python is pretty lazy and only outputs string versions of
            spec attributes.  We'll do integer and datetime conversion of
            attributes specified by the translation configuration.

            As defined in the config, we'll rename attributes to internally
            consistent names, and we'll do any necessary type conversion.
        '''

        if not self.isSpecCommand():
            raise _P4OOFatal("Unsupported Spec type %s" % self.command)

        pythonSpec = {}

        # Selectively copy p4OutputSpec attrs to mutable spec
        if 'specAttrs' in self.commandDict:
            for specAttr in self.commandDict['specAttrs']:
                p4SpecAttr = self.commandDict['specAttrs'][specAttr]
                if p4SpecAttr in p4OutputSpec:
                    if p4SpecAttr == "Change":
                        pythonSpec[specAttr] = int(p4OutputSpec[p4SpecAttr])
                    else:
                        pythonSpec[specAttr] = p4OutputSpec[p4SpecAttr]

        # Reformat date strings in Perforce objects to be more useful datetime objects
        # Date attrs cannot be modified, so don't need to be selectively copied
        if 'dateAttrs' in self.commandDict:
            for dateAttr in self.commandDict['dateAttrs']:
                p4DateAttr = self.commandDict['dateAttrs'][dateAttr]

                if p4DateAttr in p4OutputSpec:
                    if re.match(r'^\d+$', p4OutputSpec[p4DateAttr]):
                        # some query commands return epoch seconds output (e.g. clients)
                        pythonSpec[dateAttr] = datetime.fromtimestamp(float(p4OutputSpec[p4DateAttr]))
                    else:
                        # spec commands return formatted date strings local to server
                        pythonSpec[dateAttr] = datetime.strptime(p4OutputSpec[p4DateAttr], '%Y/%m/%d %H:%M:%S')

        return pythonSpec


    def translatePySpecToP4(self, pythonSpec, p4SpecDict):
        ''' Copy any modified non-date attributes to the Perforce-generated dictionary
            ignoring any date attribtues we don't modify
        '''

        if p4SpecDict is None:
            p4SpecDict = {}

        if pythonSpec is not None and 'specAttrs' in self.commandDict:

            for (specAttr,p4SpecAttr) in self.commandDict['specAttrs'].items():
                if specAttr in pythonSpec:
                    if pythonSpec[specAttr] is None:
                        if p4SpecAttr in p4SpecDict:
                            del p4SpecDict[p4SpecAttr]
                    else:
                        p4SpecDict[p4SpecAttr] = pythonSpec[specAttr]

        return p4SpecDict
