######################################################################
#  Copyright (c)2024 David L. Armstrong.
#
#  P4OO._P4PythonSchema.py
#
######################################################################

"""
Provide a set of objects that allow for interaction and translation
between P4Python output and our internally maintained Python-friendly
versions of Spec objects and Command Output.
"""

import os
import re
from datetime import datetime

import yaml
from P4OO._SpecObj import _P4OOSpecObj
from P4OO.Exceptions import P4OOFatal


class _P4OOP4PythonSchema():
    """ Class to abstract the contents of our p4Config.yml file,
        separate from the execution of the p4 commands done in
        P4OO._P4Python._P4OOP4Python
    """

    def __init__(self, configFile=None):
        self.configFile = configFile
        if self.configFile is None:
            self.configFile = os.path.dirname(__file__) + "/p4Config.yml"

        self.schemaCommands = self.readSchema(self.configFile)

    def readSchema(self, configFile):
        """ Read in our YAML p4Config.yml file and return a dict of
            supported commands as _P4OOP4PythonCommand objects
        """

        with open(configFile, 'r', encoding="utf-8") as stream:
            data = yaml.load(stream, Loader=yaml.Loader)

        return {command: _P4OOP4PythonCommand(command=command,
                                              commandDict=commandDict)
                for (command, commandDict) in data["COMMANDS"].items()}

    def getCmd(self, cmdName):

        if cmdName in self.schemaCommands:
            return self.schemaCommands[cmdName]

        raise P4OOFatal("Unsupported Command " + cmdName)

    def getSpecCmd(self, specType):

        cmdObj = self.getCmd(specType)

        if cmdObj.isSpecCommand():
            return self.schemaCommands[specType]

        raise P4OOFatal("Unsupported Spec type %s" % specType)


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

        raise P4OOFatal("Unsupported Spec type %s" % self.command)

    def getOutputType(self):
        if 'output' in self.commandDict and 'p4ooType' \
          in self.commandDict['output']:
            return self.commandDict['output']['p4ooType']

        return None

    def getOutputIdAttr(self):
        if 'output' in self.commandDict and 'idAttr' \
          in self.commandDict['output']:
            return self.commandDict['output']['idAttr']

        return None

    def getPyIdAttribute(self):

        if self.isSpecCommand():
            return self.commandDict['idAttr']

        raise P4OOFatal("Unsupported Spec type %s" % self.command)

    def getP4IdAttribute(self):

        pyIdAttr = self.getPyIdAttribute()

        return self.commandDict['specAttrs'][pyIdAttr]

    def translateP4SpecToPython(self, p4OutputSpec):
        """ Translate a P4Python provided dictionary into something more
            Python-friendly.

            P4Python is pretty lazy and only outputs string versions of
            spec attributes.  We'll do integer and datetime conversion of
            attributes specified by the translation configuration.

            As defined in the config, we'll rename attributes to internally
            consistent names, and we'll do any necessary type conversion.
        """

        if not self.isSpecCommand():
            raise P4OOFatal("Unsupported Spec type %s" % self.command)

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

        # Reformat date strings in Perforce objects to be more useful
        # datetime objects.
        # Date attrs cannot be modified, so don't need to be selectively copied
        if 'dateAttrs' in self.commandDict:
            for dateAttr in self.commandDict['dateAttrs']:
                p4DateAttr = self.commandDict['dateAttrs'][dateAttr]

                if p4DateAttr in p4OutputSpec:
                    if re.match(r'^\d+$', p4OutputSpec[p4DateAttr]):
                        # some query commands return epoch seconds output
                        # (e.g. clients)
                        pythonSpec[dateAttr] = datetime.fromtimestamp(
                            float(p4OutputSpec[p4DateAttr]))
                    else:
                        # spec commands return formatted date strings
                        # local to the server, not the client
                        pythonSpec[dateAttr] = datetime.strptime(
                            p4OutputSpec[p4DateAttr], '%Y/%m/%d %H:%M:%S')

        return pythonSpec

    def translatePySpecToP4(self, pythonSpec, p4SpecDict):
        """ Copy any modified non-date attributes to the Perforce-generated
            dictionary ignoring any date attribtues we don't modify
        """

        if p4SpecDict is None:
            p4SpecDict = {}

        if pythonSpec is not None and 'specAttrs' in self.commandDict:

            for (specAttr, p4SpecAttr) \
              in self.commandDict['specAttrs'].items():
                if specAttr in pythonSpec:
                    if pythonSpec[specAttr] is None:
                        if p4SpecAttr in p4SpecDict:
                            del p4SpecDict[p4SpecAttr]
                    else:
                        p4SpecDict[p4SpecAttr] = pythonSpec[specAttr]

        return p4SpecDict

    def getAllowedFilters(self):
        if 'queryOptions' in self.commandDict:
            return self.commandDict['queryOptions']

        return None

    def getAllowedConfigs(self):
        if 'configOptions' in self.commandDict:
            return self.commandDict['configOptions']

        return None

    def validateQuery(self, queryDict):
        """ Take a dict of name=[list] args and separate out p4 config
            arguments from command arguments.

            Validate each argument and its list of values, convert the
            list of values to p4 commandline string arguments as needed (if
            they are P4OO_ objects), and return the validated configuration
            and commandline arguments.
        """

        allowedFilters = self.getAllowedFilters()
        if allowedFilters is None:
            raise P4OOFatal("Querying not supported for Command "
                            + self.command)

        allowedConfigs = self.getAllowedConfigs() or {}

        execArgs = []
        p4Config = {}

        for (origFilterKey, queryValue) in queryDict.items():

            # none is used to remove options
            if queryValue is None:
                continue

            lcFilterKey = origFilterKey.lower()

            optionConfig = None
            isConfigOpt = False
            if lcFilterKey in allowedConfigs:
                optionConfig = allowedConfigs[lcFilterKey]
                isConfigOpt = True
            elif lcFilterKey in allowedFilters:
                optionConfig = allowedFilters[lcFilterKey]
                isConfigOpt = False
            else:
                raise P4OOFatal("Invalid Filter key: " + origFilterKey)

            optionArgs = []
            if isinstance(queryValue, (_P4OOSpecObj, int, str)):
                optionArgs.append(queryValue)
            else:
                optionArgs.extend(queryValue)

            # Check option argument types, and replace option args with
            # IDs for P4::OO objects passed in.
            # Take the opportunity to expand any Set objects we find.
            cmdOptionArgs = []
            if optionConfig is not None:

#                        'queryOptions': { 'user': { 'type': [ 'string',
#                                                              'P4OO.User.User',
#                                                            ],
#                                                    'option': '-u',
#                                                    'multiplicity': 1,
#                                                  }

                for optionArg in optionArgs:
                    matchedType = False
                    if 'type' not in optionConfig:
                        matchedType = True
                    else:
                        for checkType in optionConfig['type']:
                            if matchedType:
                                break

                            if checkType == "string":
                                if isinstance(optionArg, str):
                                    cmdOptionArgs.append(optionArg)
                                    matchedType = True
                            elif checkType == "integer":
                                if isinstance(optionArg, int):
                                    cmdOptionArgs.append(optionArg)
                                    matchedType = True
                            else:
                                # Must be a P4OO type!  To check P4OO types, we need to import.

                                # First, break down setType/SpecType from the checkType to perform the import
                                m = re.match(r'^(.+)Set$', checkType)
                                if m:
                                    specType = m.group(1)
                                    setType = checkType
                                else:
                                    specType = checkType
                                    setType = checkType + "Set"

                                # Second, import specType and SetType
# TODO need to look into this issue
#                                specModule = __import__("P4OO." + specType, globals(), locals(), ["P4OO" + specType, "P4OO" + setType], -1)
                                specModule = __import__("P4OO." + specType, globals(), locals(), ["P4OO" + specType, "P4OO" + setType], 0)
                                specClass = getattr(specModule, "P4OO" + specType)
                                setClass = getattr(specModule, "P4OO" + setType)

                                # Third, do the actual type check and append optionArgs as appropriate
                                if checkType == setType and isinstance(optionArg, setClass):
                                    # Special Set expansion...this gets weird, eh?
                                    cmdOptionArgs.extend(optionArg.listObjectIDs())
                                    matchedType = True

                                elif checkType == specType and isinstance(optionArg, specClass):
                                    cmdOptionArgs.append(optionArg._uniqueID())
                                    matchedType = True

                    if not matchedType:
                        # Looped through all types, didn't find a match
                        raise P4OOFatal("Got %r, but filter key '%s' accepts arguments of only these types: "
                                        % (optionArg, origFilterKey) + ", ".join(optionConfig['type']))

#            print("optionConfig: ", optionConfig)
            # defined cmdline options go at the front
            if 'multiplicity' in optionConfig and optionConfig['multiplicity'] == 0:
                if len(cmdOptionArgs) != 0:
                    raise P4OOFatal("Filter key: %s accepts no arguments.\n" % origFilterKey)

                if isConfigOpt:
                    p4Config[optionConfig['option']] = True
                else:
                    execArgs.insert(0, optionConfig['option'])

            elif 'multiplicity' in optionConfig and optionConfig['multiplicity'] == 1:
                if len(cmdOptionArgs) != 1:
                    raise P4OOFatal("Filter key: %s accepts exactly 1 argument.\n" % origFilterKey)

                if 'bundledArgs' in optionConfig and optionConfig['bundledArgs'] is not None:
                    # join the option and its args into one string  ala "-j8"
                    bundledArg = optionConfig['option'] + "".join(cmdOptionArgs)
                    execArgs.insert(0, bundledArg)
# TODO - ignoring p4Config here because it won't be needed... I think
                else:
                    if isConfigOpt:
                        p4Config[optionConfig['option']] = cmdOptionArgs[0]
                    else:
                        # "unshift" one at a time in reverse order
                        for arg in reversed(cmdOptionArgs):
                            execArgs.insert(0, arg)
                        execArgs.insert(0, optionConfig['option'])
            else:
                if 'option' in optionConfig:
# TODO - ignoring p4Config here because it won't be needed... I think
                    execArgs.append(optionConfig['option'])
                execArgs.extend(cmdOptionArgs)

        return (execArgs, p4Config)
