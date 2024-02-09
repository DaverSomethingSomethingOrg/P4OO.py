######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#  Copyright (c)2012-2013, Cisco Systems, Inc.
#
#  P4OO._Connection.P4Python.py
#
######################################################################

#NAME / DESCRIPTION
'''
P4OO interface to P4Python

P4OO._Connection.P4Python provides the translation from P4OO
data-object calls into P4 subcommands, and translation of p4
subcommand output back into P4OO data-objects.
'''

######################################################################
# Includes
#
# For the YAML config file
import os
import re
import datetime
import yaml

# P4Python
from P4 import P4,P4Exception,Spec

from P4OO._Base import _P4OOBase
from P4OO._Exceptions import _P4OOFatal, _P4Fatal, _P4Warning
from P4OO._Connection import _P4OOConnection
from P4OO._SpecObj import _P4OOSpecObj


######################################################################
# P4Python Class Initialization
#
class _P4OOP4Python(_P4OOConnection):
    ######################################################################
    # Globals
    #
    _P4PYTHON_COMMAND_TRANSLATION = None

    ######################################################################
    # Methods
    #


    ######################################################################
    # readCounter(name)
    #
    # NOTES:
    #
    def readCounter(self, counterName):
        '''Read the named counter from Perforce and return the value'''

        # Make sure we've read in the config file
        self._initialize()

        p4Output = self._execCmd("counter", counterName)
        try:
            return int(p4Output[0]['value'])
        except ValueError:
            return p4Output[0]['value']

    ######################################################################
    # setCounter(name, newValue)
    #
    # NOTES:
    #
    def setCounter(self, counterName, newValue):
        '''Set the named counter in Perforce'''

        # Make sure we've read in the config file
        self._initialize()

        p4Output = self._execCmd("counter", counterName, newValue)
        try:
            return int(p4Output[0]['value'])
        except ValueError:
            return p4Output[0]['value']


    ######################################################################
    # refreshSpec( specObj )
    #
    # NOTES:
    # - Since modifiedSpec is wiped out, any changes made via _setSpecAttr
    #   will be lost!
    #
    def refreshSpec(self, specObj):
        '''Clear the cached objects and modifiedSpec and re-read spec from Perforce'''

        specObj._delAttr('p4SpecObj')
        specObj._delAttr('modifiedSpec')
        self.readSpec(specObj)


    ######################################################################
    # readSpec( specObj )
    #
    # NOTES:
    # - If the spec has already been read and is present, no action is taken.
    #
    def readSpec(self, specObj):
        ''' Query Perforce for the specified object's spec and load it into
            the provided object doing any appropriate data conversions along the way.
        '''

        # Make sure we've read in the config file
        self._initialize()

        specType = specObj._SPECOBJ_TYPE
        specID = specObj._getAttr('id')
        p4SpecObj = specObj._getAttr('p4SpecObj')

        # We only read if not already read.  Use refreshSpec to re-read.
        if p4SpecObj is None:
            if specType not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION:
                raise _P4OOFatal("Unsupported Spec type %s" % specType)

            # Nothing to do here, no id in any form from caller
            if specID is None and _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['idRequired']:
                return False

            specCmd = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specCmd']

            p4Output = self._execCmd(specCmd, "-o", specID)

            # Since we muck with the Spec replacing date fields with datetime objects, we just flatten the objects.
            p4SpecObj = p4Output[0]
            specObj._setAttr('p4SpecObj', p4SpecObj)

        p4Spec = dict(p4SpecObj)
        self._generateModifiedSpec(specObj, p4Spec)


    def _generateModifiedSpec(self, specObj, specDict):
        # Perforce will return an "empty" spec when a specified object isn't found so it can be handily created.
        # We don't want that behavior here, so we throw an exception instead.
        # We'll want to have a "createSpec" method for that kind of thing
        # HACK - Specs that don't have 'Update' timestamp are specs that don't exist yet.
        # HACKHACK - change is exceptional in this regard. :)
#HACKHACKHACK want to comment this out to leverage default specs, but other stuff breaks right now.
#TODO fix this somehow
#        if specType is not 'change' and 'Update' not in p4Spec:
#            raise _P4OOFatal(specType + ": " + str(specID) + " does not exist")
#            return None

        specType = specObj._SPECOBJ_TYPE
        specID = specObj._getAttr('id')

        # Here we take the spec from P4 and make it something useful
        modifiedSpec = specObj._getAttr('modifiedSpec')
        if modifiedSpec is None:
            modifiedSpec = {}

        # Selectively copy specDict attrs to mutable spec
        if 'specAttrs' in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]:
            for specAttr in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specAttrs']:
                # ignore attributes already set by caller
                if specAttr not in modifiedSpec:
                    p4SpecAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specAttrs'][specAttr]
                    if p4SpecAttr in specDict:
                        if p4SpecAttr == "Change":
                            modifiedSpec[specAttr] = int(specDict[p4SpecAttr])
                        else:
                            modifiedSpec[specAttr] = specDict[p4SpecAttr]

        # Reformat date strings in Perforce objects to be more useful datetime objects
        # Date attrs cannot be modified, so don't need to be selectively copied
        if 'dateAttrs' in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]:
            for dateAttr in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['dateAttrs']:
                p4DateAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['dateAttrs'][dateAttr]

                if p4DateAttr in specDict:
                    if re.match(r'^\d+$', specDict[p4DateAttr]):
                        # some query commands return epoch seconds output (e.g. clients)
                        modifiedSpec[dateAttr] = datetime.datetime.fromtimestamp(float(specDict[p4DateAttr]))
                    else:
                        # spec commands return formatted date strings local to server
                        modifiedSpec[dateAttr] = datetime.datetime.strptime(specDict[p4DateAttr], '%Y/%m/%d %H:%M:%S')

        specObj._setAttr('modifiedSpec', modifiedSpec)

        # We'll set the object's specID if it was not defined..if we can.
        if specID is None:
            idAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['idAttr']
#            p4IdAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specAttrs'][idAttr]

            # At this point the SpecObj is initialized enough for this to work...
#            specObj._setAttr('id', specDict[p4IdAttr] )
            specObj._setAttr('id', modifiedSpec[idAttr] )
                

        return True


# TODO...
    def saveSpec(self, specObj, force=False):
        specType = specObj._SPECOBJ_TYPE
        specID = specObj._getAttr('id')

        # Make sure we've read in the config file
        self._initialize()

        if specType not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION:
            raise _P4OOFatal("Unsupported Spec type %s" % specType)

        specCmd = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specCmd']

        p4SpecObj = specObj._getAttr('p4SpecObj')
        modifiedSpec = specObj._getAttr('modifiedSpec')

        # If there's no modified spec or ID, then there's nothing to save
#        if modifiedSpec is None and specID is None:
#TODO throw an exception?
#            return False

        # If specObj isn't already initialized (it should be), then initialize it.
        if p4SpecObj is None:
            # We need specID first here to initialize empty spec properly.. see if we have it in modifiedSpec
            if specID is None and modifiedSpec is not None:
                idAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['idAttr']
                if idAttr in modifiedSpec:
                    specID = specObj._setAttr('id', modifiedSpec[idAttr] )

            try:
                self.readSpec(specObj)
            except P4Exception:
                # Ignore exceptions for objects that don't exist, we might be creating them here
                pass

            # refresh the local variables for spec after read
            specID = specObj._getAttr('id')
            p4SpecObj = specObj._getAttr('p4SpecObj')
            modifiedSpec = specObj._getAttr('modifiedSpec')

        if p4SpecObj is None:
            # This must be a brand new spec
            p4SpecObj = Spec()

        # Copy any modified non-date attributes to the Perforce-generated dictionary
        # ignoring any date attribtues we don't modify
        if modifiedSpec is not None:
            if 'specAttrs' in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]:
                for specAttr in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specAttrs']:
                    p4SpecAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specAttrs'][specAttr]
                    if specAttr in modifiedSpec:
                        if modifiedSpec[specAttr] is None:
                            if p4SpecAttr in p4SpecObj:
                                del p4SpecObj[p4SpecAttr]
                        else:
                            p4SpecObj[p4SpecAttr] = modifiedSpec[specAttr]

        # If we need a specID, we need a specID...
        idAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['idAttr']
        p4IdAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specAttrs'][idAttr]

        if p4IdAttr in p4SpecObj:
            # We'll set the object's specID if it was not defined..if we can.
            if specID is None:
                # At this point the SpecObj is initialized enough for this to work...
                specObj._setAttr('id', p4SpecObj[p4IdAttr] )
        else:
            if _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['idRequired']:
                if specID is not None:
                    p4SpecObj[p4IdAttr] = specID
                else:
                    p4SpecObj[p4IdAttr] = "new"
#TODO be throwing exceptions...

        p4Output = None
        if force:
            if "forceOption" not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]:
                raise _P4OOFatal("Command %s doesn't support force" % (cmdName,) )

            p4Output = self._execCmd(specCmd, "-i", p4SpecObj, "-f")
        else:
            p4Output = self._execCmd(specCmd, "-i", p4SpecObj)

        # Since we know we're saving a spec, we can take some liberties with hardcoded parsing here.
        if specID is None:
            if specType == "change":
                # parse p4Output for new change#
                # ['Change 1 created.']
                specID = re.search(r'Change (\d+) created', p4Output[0]).group(1)
#TODO...
#                print("specID: ", specID)
            specObj._setAttr('id', specID )
#TODO... other spec types that accept new?

        # refresh our object against the freshly saved spec to get updated timestamps and so on
        self.refreshSpec(specObj)

        return True


    def deleteSpec(self, specObj, force=False):
        specType = specObj._SPECOBJ_TYPE
        specID = specObj._getAttr('id')

        # Make sure we've read in the config file
        self._initialize()

        if specType not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION:
            raise _P4OOFatal("Unsupported Spec type %s" % specType)

        specCmd = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specCmd']

        p4SpecObj = specObj._getAttr('p4SpecObj')
        modifiedSpec = specObj._getAttr('modifiedSpec')

        # If there's no modified spec or ID, then there's nothing to save
        if modifiedSpec is None and specID is None:
#TODO throw an exception?
            return False

        # If specObj isn't already initialized (it should be), then initialize it.
        if p4SpecObj is None:
            # We need specID first here to initialize empty spec properly.. see if we have it in modifiedSpec
            if specID is None and modifiedSpec is not None:
                idAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['idAttr']
                if idAttr in modifiedSpec:
                    specID = specObj._setAttr('id', modifiedSpec[idAttr] )

            try:
                self.readSpec(specObj)
            except P4Exception:
                # Ignore exceptions for objects that don't exist, we might be creating them here
                pass

            # refresh the local variables for spec after read
            specID = specObj._getAttr('id')
            p4SpecObj = specObj._getAttr('p4SpecObj')
            modifiedSpec = specObj._getAttr('modifiedSpec')

        if p4SpecObj is None:
            # This must be a brand new spec... nothing to delete
            return False

        # If we need a specID, we need a specID...
        idAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['idAttr']
        p4IdAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]['specAttrs'][idAttr]

        if specID is None:
            # We'll set the object's specID if it was not defined..if we can.
            if p4IdAttr in p4SpecObj:
                # At this point the SpecObj is initialized enough for this to work...
                specObj._setAttr('id', p4SpecObj[p4IdAttr] )
                specID = p4SpecObj[p4IdAttr]
#TODO be throwing exceptions...

        p4Output = None
        if force:
            if "forceOption" not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[specType]:
                raise _P4OOFatal("Command %s doesn't support force" % (cmdName,) )

            p4Output = self._execCmd(specCmd, "-d", "-f", specID)
        else:
            p4Output = self._execCmd(specCmd, "-d", specID)

        # If we made it this far, nothing fatal happened inside Perforce, but spec was not necessarily deleted.
#TODO I'm just guessing that all spec deletions follow this format of "^p4IdAttr specID (can't be )?deleted.$"
        m = re.match(r'^%s %s (.*)deleted.$' % (re.escape(p4IdAttr), re.escape(specID)), p4Output[0])
        if not m or m.group(1) != '':
            raise _P4OOFatal(p4Output)

        return True


    def runCommand(self, cmdName, **kwargs):
        query = dict(kwargs)

        # Make sure we've read in the config file
        self._initialize()

        if cmdName not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION:
            raise _P4OOFatal("Unsupported Command " + cmdName)

        if 'queryOptions' not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]:
            raise _P4OOFatal("Querying not supported for Command " + cmdName)

        allowedFilters = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]['queryOptions']

        allowedConfigs = {}
        if 'configOptions' in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]:
            allowedConfigs = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]['configOptions']

        # TODO - this sucks, but hey...
        p4Config = {}
        rawOutput = False
        if 'rawOutput' in query:
            rawOutput = query['rawOutput']
            # We also turn off tagged output when raw is requested!
            p4Config['tagged'] = 0
            del query['rawOutput']


        execArgs = []
        for origFilterKey in query.keys():

            # none is used to remove options
            if query[origFilterKey] is None:
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
                raise _P4OOFatal("Invalid Filter key: " + origFilterKey)

            optionArgs = []
            if isinstance(query[origFilterKey], str) or isinstance(query[origFilterKey], int) or isinstance(query[origFilterKey], _P4OOSpecObj):
                optionArgs.append(query[origFilterKey])
            else:
                optionArgs.extend(query[origFilterKey])

            # Check option argument types, and replace option args with IDs for P4::OO objects passed in
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
#TODO need to look into this issue
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
                        raise _P4OOFatal("Got %r, but filter key '%s' accepts arguments of only these types: " % (optionArg, origFilterKey)
                                                 + ", ".join(optionConfig['type']) )

#            print("optionConfig: ", optionConfig )
            # defined cmdline options go at the front
            if 'multiplicity' in optionConfig and optionConfig['multiplicity'] == 0:
                if len(cmdOptionArgs) != 0:
                    raise _P4OOFatal("Filter key: %s accepts no arguments.\n" % origFilterKey )

                if isConfigOpt:
                    p4Config[optionConfig['option']] = True
                else:
                    execArgs.insert(0, optionConfig['option'])

            elif 'multiplicity' in optionConfig and optionConfig['multiplicity'] == 1:
                if len(cmdOptionArgs) != 1:
                    raise _P4OOFatal("Filter key: %s accepts exactly 1 argument.\n" % origFilterKey )

                if 'bundledArgs' in optionConfig and optionConfig['bundledArgs'] is not None:
# join the option and its args into one string  ala "-j8"
                    bundledArg = optionConfig['option'] + "".join(cmdOptionArgs)
                    execArgs.insert(0, bundledArg)
#TODO - ignoring p4Config here because it won't be needed... I think
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
#TODO - ignoring p4Config here because it won't be needed... I think
                    execArgs.append(optionConfig['option'])
                execArgs.extend(cmdOptionArgs)

#        print("p4Config: ", p4Config )
        p4Out = self._execCmd(cmdName, execArgs, **p4Config)
## TODO... subcommands?
##                'counter' => { 'specCmd'      => 'counter',
##                               'singularID'   => 'counter',
##                               'queryCmd'     => 'counters',
##                               'pluralID'     => 'counter',
##                               'idAttr'       => 'counter',
##     p4 counter name
##     p4 counter [-f] name value
##     p4 counter [-f] -d name
##     p4 counter [-i] name
##
###subcommands:
### increment
### delete
### set
##                            },

        # If no special output massaging is needed, we're done!
        if rawOutput or 'output' not in _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]:
            return p4Out

        return self._parseOutput(cmdName, p4Out)


    def _parseOutput(self, cmdName, p4Out):

        # Make sure we've read in the config file
        self._initialize()

        p4ooType = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]['output']['p4ooType']
        setType = p4ooType + "Set"
        idAttr = _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]['output']['idAttr']
#        singularID = _P4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]['output']['singularID']

        # Make sure the caller is properly equipped to use any objects
        # we construct here.
#        specModule = __import__("P4OO." + p4ooType, globals(), locals(), ["P4OO" + p4ooType, "P4OO" + setType], -1)
        specModule = __import__("P4OO." + p4ooType, globals(), locals(), ["P4OO" + p4ooType, "P4OO" + setType], 0)
#        setModule = __import__("P4OO." + setType, globals(), locals(), ["P4OO" + setType], -1)
        specClass = getattr(specModule, "P4OO" + p4ooType)
        setClass = getattr(specModule, "P4OO" + setType)

        objectList = []

        # Don't really care about the content of the output, just the specIDs.
        for p4OutHash in p4Out:
            if idAttr not in p4OutHash:
                raise _P4OOFatal("Unexpected output from Perforce.")

            # Copy the idAttr output value to the id attribute
            #  if they aren't one and the same already
#            if singularID is not idAttr:
#                p4OutHash[singularID] = p4OutHash[idAttr]

            # HACK - Instead of eval'ing this through the type's
            # constructor, we'll just use the base class and bless
#            specAttrs = { 'p4Spec':  p4OutHash,
#                          'id':      p4OutHash[idAttr],
#                          '_p4Conn': self,  # Make sure each of these objects can reuse this connection too
#                        }
#            specObj = eval( singularType + "(specAttrs)" )


            specObj = specClass()

#TODO - figure out P4.Spec objects
#            specObj._setAttr('p4Spec', Spec(p4OutHash))
#TODO - need to fix this special case for Change - need better construction logic
            if p4ooType == 'Change':
                specObj._setAttr('id', int(p4OutHash[idAttr]))
            else:
                specObj._setAttr('id', p4OutHash[idAttr])

#TODO - This is a little awkward...
            if isinstance(specObj, _P4OOSpecObj):
                self._generateModifiedSpec(specObj, p4OutHash)
#            specObj._setAttr('modifiedSpec', p4OutHash)
#            self._logDebug( "id: ", p4OutHash[idAttr])

            specObj._setAttr('_p4Conn', self)  # Make sure each of these objects can reuse this connection too
            objectList.append(specObj)

        # Wrap it with a bow
        setObj = setClass()

        setObj._setAttr('_p4Conn', self)
        setObj.addObjects(objectList)
        return setObj

    ######################################################################
    # Internal Methods
    #
    def _execCmd(self, p4SubCmd, *args, **p4Config):

        # We want this pretty much right from the start
        p4PythonObj = self._connect()

        # copy the input tuple to a mutable list first.
        listArgs = list(args)

#TODO - listArgs is an immutable tuple in P4Python...
        if len(listArgs) > 0:
            # First strip undef args from the tail, P4PERL don't like them
            while listArgs[-1] is None or listArgs[-1] == "":
                del listArgs[-1]

            # Next look for a '-i' arg for setting input and exrtact the input arg
            try:
                inputIndex = listArgs.index("-i")
                p4PythonObj.input = listArgs[inputIndex+1]
                listArgs = listArgs[:inputIndex+1]+listArgs[inputIndex+2:]
            except ValueError:
                pass


#            if listArgs[0] == "-i":
#                p4PythonObj.input = listArgs[1]
#                self._logDebug("Setting Input:", p4PythonObj.input)
#                listArgs = listArgs[2:]


        # override p4Python settings for this command as applicable
        origConfig = {}
        for var in p4Config:
            origConfig[var] = p4PythonObj.__getattribute__(var)
            p4PythonObj.__setattr__(var, p4Config[var])
            self._logDebug("overriding p4Config['%s'] = %s with %s" % (var, str(origConfig[var]), str(p4Config[var])))

# TODO ping server before each command?
        self._logDebug("Executing:", p4SubCmd, listArgs)
        p4Out = p4PythonObj.run(p4SubCmd, listArgs)
        self._logDebug("p4Out: ", p4Out)

        # restore p4Python settings changed for this command only
        for var in p4Config:
            p4PythonObj.__setattr__(var, origConfig[var])
            self._logDebug("resetting p4Config['%s'] = %s" % (var, str(origConfig[var])))

# TODO Should do something to detect disconnects, etc.

        # If we have errors and warnings, we want to give both to caller
        if len(p4PythonObj.errors) > 0:
            errMsg = "ERROR: " + "".join(p4PythonObj.errors)

            if len(p4PythonObj.warnings) > 0:
                errMsg += "\nWARNING: " + "".join(p4PythonObj.warnings)

            raise _P4Fatal("P4 Command Failed:\n" + errMsg)

        if len(p4PythonObj.warnings) > 0:
            warnMsg = "WARNING: " + "".join(p4PythonObj.warnings)
            raise _P4Warning("P4 Command Warned:\n" + warnMsg)

        return p4Out


    def _connect(self):
        p4PythonObj = self._getAttr('p4PythonObj')

        if p4PythonObj is None:
            p4PythonObj = P4()
            try:
                p4PythonObj.connect()
                p4PythonObj.exception_level = 0
            except P4Exception:
                raise _P4Fatal("P4 Connection Failed")

            self._setAttr('p4PythonObj', p4PythonObj)
            self._setAttr('_ownP4PythonObj', 1)

        return p4PythonObj


    def _disconnect(self):
        ownP4PythonObj = self._getAttr('_ownP4PythonObj')

        if ownP4PythonObj:
            # We instantiated the connection, so we'll tear it down too
            p4PythonObj = self._getAttr('p4PythonObj')

            if p4PythonObj is not None:
                p4PythonObj.disconnect()

        self._setAttr('_ownP4PythonObj', None)
        self._setAttr('p4PythonObj', None)
        return True

    def _initialize(self):
        if _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION is None:
            configFile = os.path.dirname(__file__) + "/p4Config.yml"
            stream = open(configFile, 'r')
            data = yaml.load(stream, Loader=yaml.Loader)
            _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION = data["COMMANDS"]
            stream.close()

        return True

    def __del__(self):
        self._disconnect()
        return True


# read in the YAML config file with our command translation table
class _P4OOP4PythonConfig(_P4OOBase):

    _P4PYTHON_COMMAND_TRANSLATION = None

    def __init__(self, **kwargs ):
        self._objAttrs = kwargs

    def readConfig(self, configFile):
        if _P4OOP4PythonConfig._P4PYTHON_COMMAND_TRANSLATION is None:
            configFile = os.path.dirname(__file__) + "/p4Config.yml"
            stream = open(configFile, 'r')
            data = yaml.load(stream, Loader=yaml.Loader)
            _P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION = data["COMMANDS"]
            stream.close()
    