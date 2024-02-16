######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#  Copyright (c)2012-2013, Cisco Systems, Inc.
#
#  P4OO._P4Python.py
#
######################################################################

import os
import re

# P4Python
from P4 import P4, P4Exception, Spec

from P4OO.Exceptions import P4OOFatal, P4Fatal, P4Warning
from P4OO._Connection import _P4OOConnection
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._P4PythonSchema import _P4OOP4PythonSchema


class _P4OOP4Python(_P4OOConnection):

    def readCounter(self, counterName):
        ''' Read the named counter from Perforce and return the value. '''

        # Make sure we've read in the config file
        self._initialize()

        p4Output = self._execCmd("counter", counterName)
        try:
            return int(p4Output[0]['value'])
        except ValueError:
            return p4Output[0]['value']

    def setCounter(self, counterName, newValue):
        ''' Set the named counter in Perforce. '''

        # Make sure we've read in the config file
        self._initialize()

        p4Output = self._execCmd("counter", counterName, newValue)
        try:
            return int(p4Output[0]['value'])
        except ValueError:
            return p4Output[0]['value']

    def refreshSpec(self, specObj):
        ''' Clear the cached objects and modifiedSpec and re-read spec
            from Perforce.

            Any changes made via _setSpecAttr will be lost!
        '''

        specObj._delAttr('p4SpecObj')
        specObj._delAttr('modifiedSpec')
        self.readSpec(specObj)

    def readSpec(self, specObj):
        ''' Query Perforce for the specified object's spec and load it
            into the provided object doing any appropriate data conversions
            along the way.

            If the spec has already been read and is present, no action
            is taken.
        '''

        # Make sure we've read in the config file
        self._initialize()

        specType = specObj._SPECOBJ_TYPE
        specID = specObj._getAttr('id')
        p4SpecObj = specObj._getAttr('p4SpecObj')
        modifiedSpec = specObj._getAttr('modifiedSpec')

        specCmdObj = self._p4PythonSchema.getSpecCmd(specType=specType)
        idAttr = specCmdObj.getPyIdAttribute()

        # We only read if not already read.  Use refreshSpec to re-read.
        if p4SpecObj is None:
            if specID is None and specCmdObj.isIdRequired():
                if modifiedSpec is not None and idAttr in modifiedSpec:
                    specID = specObj._setAttr('id', modifiedSpec[idAttr])
                else:
                    # Nothing to do here, no id in any form from caller
                    raise P4OOFatal("Cannot identify %s object" %
                                    (specType,))

            specCmd = specCmdObj.getSpecCmd()
            p4Output = self._execCmd(specCmd, "-o", specID)

            # Since we muck with the Spec replacing date fields with
            # datetime objects, we just flatten the objects.
            p4SpecObj = p4Output[0]
            specObj._setAttr('p4SpecObj', p4SpecObj)

        p4Spec = dict(p4SpecObj)
        return self._generateModifiedSpec(specCmdObj, specObj, p4Spec)

    def _generateModifiedSpec(self, specCmdObj, specObj, specDict):
        # Perforce will return an "empty" spec when a specified object isn't
        # found so it can be handily created.
        # We don't want that behavior here, so we throw an exception instead.
        # We'll want to have a "createSpec" method for that kind of thing.

# HACK - Specs that don't have 'Update' timestamp are specs that don't exist yet.
# HACKHACK - change is exceptional in this regard. :)
# HACKHACKHACK want to comment this out to leverage default specs, but other stuff breaks right now.
# TODO fix this somehow
#        if specType is not 'change' and 'Update' not in p4Spec:
#            raise P4OOFatal(specType + ": " + str(specID) + " does not exist")
#            return None

        specID = specObj._getAttr('id')

        # Here we take the spec from P4 and make it something useful
        modifiedSpec = specObj._getAttr('modifiedSpec')
        if modifiedSpec is None:
            modifiedSpec = {}

        # merge specDict from P4Python and modifiedSpec
        pythonSpecDict = specCmdObj.translateP4SpecToPython(specDict)

        for specAttr in pythonSpecDict:
            # ignore attributes already set by caller
            if specAttr not in modifiedSpec:
                modifiedSpec[specAttr] = pythonSpecDict[specAttr]

        specObj._setAttr('modifiedSpec', modifiedSpec)

        # We'll set the object's specID if it was not defined..if we can.
        if specID is None:
            idAttr = specCmdObj.getPyIdAttribute()
            specObj._setAttr('id', modifiedSpec[idAttr])

        return modifiedSpec

    def saveSpec(self, specObj, force=False):
# TODO Document this...

        # Start with readSpec to make sure we're in sync with the server
        self.readSpec(specObj)

        specType = specObj._SPECOBJ_TYPE
        specID = specObj._getAttr('id')

        specCmdObj = self._p4PythonSchema.getSpecCmd(specType=specType)
        specCmd = specCmdObj.getSpecCmd()

        p4SpecObj = specObj._getAttr('p4SpecObj')
        modifiedSpec = specObj._getAttr('modifiedSpec')

        # If there's no modified spec or ID, then there's nothing to save
        if modifiedSpec is None and specID is None:
            raise P4OOFatal("Cannot save %s object: Nothing to save" %
                            (specType,))

        if p4SpecObj is None:
            # This must be a brand new spec
            p4SpecObj = Spec()

        specCmdObj.translatePySpecToP4(modifiedSpec, p4SpecObj)

        # If we need a specID, we need a specID...
        p4IdAttr = specCmdObj.getP4IdAttribute()

        if p4IdAttr in p4SpecObj:
            # We'll set the object's specID if it was not defined..if we can.
            if specID is None:
                # At this point the SpecObj is initialized enough for
                # this to work...
                specObj._setAttr('id', p4SpecObj[p4IdAttr])
        else:
            if specCmdObj.isIdRequired():
                if specID is not None:
                    p4SpecObj[p4IdAttr] = specID
                else:
                    p4SpecObj[p4IdAttr] = "new"

        p4Output = None
        if force:
            if not specCmdObj.isForceable():
                raise P4OOFatal("Command %s doesn't support force" %
                                (specCmd,))

# TODO hardcoded forceoption should be config produced..
            p4Output = self._execCmd(specCmd, "-i", p4SpecObj, "-f")
        else:
            p4Output = self._execCmd(specCmd, "-i", p4SpecObj)

        # Since we know we're saving a spec, we can take some liberties
        # with hardcoded parsing here.
        if specID is None:
            if specType == "change":
                # parse p4Output for new change#
                # ['Change 1 created.']
                specID = re.search(r'Change (\d+) created',
                                   p4Output[0]).group(1)
# TODO...
#                print("specID: ", specID)
            specObj._setAttr('id', specID)
# TODO... other spec types that accept new?

        # refresh our object against the freshly saved spec to get updated
        # timestamps and so on
        self.refreshSpec(specObj)

        return True

    def deleteSpec(self, specObj, force=False):
        specType = specObj._SPECOBJ_TYPE
        specID = specObj._getAttr('id')

        # Make sure we've read in the config file
        self._initialize()

        specCmdObj = self._p4PythonSchema.getSpecCmd(specType=specType)
        idAttr = specCmdObj.getPyIdAttribute()
        specCmd = specCmdObj.getSpecCmd()

        p4SpecObj = specObj._getAttr('p4SpecObj')
        modifiedSpec = specObj._getAttr('modifiedSpec')

        # If there's no modified spec or ID, then there's nothing to save
        if modifiedSpec is None and specID is None:
# TODO throw an exception?
            return False

        # If specObj isn't already initialized (it should be), then
        # initialize it.
        if p4SpecObj is None:
            # We need specID first here to initialize empty spec properly..
            # see if we have it in modifiedSpec
            if specID is None and modifiedSpec is not None:
                if idAttr in modifiedSpec:
                    specID = specObj._setAttr('id', modifiedSpec[idAttr])

            try:
                self.readSpec(specObj)
            except P4Exception:
                # Ignore exceptions for objects that don't exist, we might
                # be creating them here
                pass

            # refresh the local variables for spec after read
            specID = specObj._getAttr('id')
            p4SpecObj = specObj._getAttr('p4SpecObj')
            modifiedSpec = specObj._getAttr('modifiedSpec')

        if p4SpecObj is None:
            # This must be a brand new spec... nothing to delete
            return False

        # If we need a specID, we need a specID...
        p4IdAttr = specCmdObj.getP4IdAttribute()

        if specID is None:
            # We'll set the object's specID if it was not defined..if we can.
            if p4IdAttr in p4SpecObj:
                # At this point the SpecObj is initialized enough for this
                # to work...
                specObj._setAttr('id', p4SpecObj[p4IdAttr])
                specID = p4SpecObj[p4IdAttr]
# TODO be throwing exceptions...

        p4Output = None
        if force:
            if not specCmdObj.isForceable():
                raise P4OOFatal("Command %s doesn't support force" %
                                (specCmd,))

# TODO hardcoded forceoption should be config produced..
            p4Output = self._execCmd(specCmd, "-d", "-f", specID)
        else:
            p4Output = self._execCmd(specCmd, "-d", specID)

        # If we made it this far, nothing fatal happened inside Perforce,
        # but spec was not necessarily deleted.
# TODO I'm just guessing that all spec deletions follow this format of "^p4IdAttr specID (can't be )?deleted.$"
        m = re.match(r'^%s %s (.*)deleted.$' % (re.escape(p4IdAttr),
                                                re.escape(specID)),
                     p4Output[0])
        if not m or m.group(1) != '':
            raise P4OOFatal(p4Output)

        return True

    def runCommand(self, cmdName, rawOutput=False, **kwargs):
        ''' Wrapper around _execCmd that orchestrates validating the
            commandline arguments from P4OO Spec/Set objects, executing
            the command through P4Python, and parsing the returned output
            back into P4OO Spec/Set objects.
        '''
        query = dict(kwargs)

        # Make sure we've read in the config file
        self._initialize()

        cmdObj = self._p4PythonSchema.getCmd(cmdName=cmdName)

        (execArgs, p4Config) = cmdObj.validateQuery(query)

        if rawOutput:
            # We also turn off tagged output when raw is requested!
            p4Config['tagged'] = 0

#        print("p4Config: ", p4Config )
        p4Out = self._execCmd(cmdName, execArgs, **p4Config)

# TODO... subcommands?
#                'counter' => { 'specCmd'      => 'counter',
#                               'singularID'   => 'counter',
#                               'queryCmd'     => 'counters',
#                               'pluralID'     => 'counter',
#                               'idAttr'       => 'counter',
#     p4 counter name
#     p4 counter [-f] name value
#     p4 counter [-f] -d name
#     p4 counter [-i] name
#
# subcommands:
#  increment
#  delete
#  set
#                            },

        # If no special output massaging is needed, we're done!

        if rawOutput or cmdObj.getOutputType() is None:
            return p4Out

        return self._parseOutput(cmdName, p4Out)

    def _parseOutput(self, cmdName, p4Out):

        # Make sure we've read in the config file
        self._initialize()
        cmdObj = self._p4PythonSchema.getCmd(cmdName=cmdName)

        p4ooType = cmdObj.getOutputType()
        setType = p4ooType + "Set"
        idAttr = cmdObj.getOutputIdAttr()
#        singularID = _P4Python._P4PYTHON_COMMAND_TRANSLATION[cmdName]['output']['singularID']

        # Make sure the caller is properly equipped to use any objects
        # we construct here.
#        specModule = __import__("P4OO." + p4ooType, globals(), locals(),
#                                ["P4OO" + p4ooType, "P4OO" + setType], -1)
        specModule = __import__("P4OO." + p4ooType, globals(), locals(),
                                ["P4OO" + p4ooType, "P4OO" + setType], 0)
#        setModule = __import__("P4OO." + setType, globals(), locals(),
#                               ["P4OO" + setType], -1)
        specClass = getattr(specModule, "P4OO" + p4ooType)
        setClass = getattr(specModule, "P4OO" + setType)

        objectList = []

        # Don't really care about the content of the output, just the specIDs.
        for p4OutHash in p4Out:
            if idAttr not in p4OutHash:
                raise P4OOFatal("Unexpected output from Perforce.")

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

# TODO - figure out P4.Spec objects
#            specObj._setAttr('p4Spec', Spec(p4OutHash))
# TODO - need to fix this special case for Change - need better construction logic
            if p4ooType == 'Change':
                specObj._setAttr('id', int(p4OutHash[idAttr]))
            else:
                specObj._setAttr('id', p4OutHash[idAttr])

# TODO - This is a little awkward...
            if isinstance(specObj, _P4OOSpecObj):
                specCmdObj = self._p4PythonSchema.getSpecCmd(
                    specType=specObj._SPECOBJ_TYPE)
                self._generateModifiedSpec(specCmdObj, specObj, p4OutHash)
#            specObj._setAttr('modifiedSpec', p4OutHash)
#            self._logDebug( "id: ", p4OutHash[idAttr])

            # Make sure each of these objects can reuse this connection too
            specObj._setAttr('_p4Conn', self)
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

# TODO - listArgs is an immutable tuple in P4Python...
        if len(listArgs) > 0:
            # First strip undef args from the tail, P4PERL don't like them
            while listArgs[-1] is None or listArgs[-1] == "":
                del listArgs[-1]

            # Next look for a '-i' arg for setting input and extract the arg
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
        for (var, value) in p4Config.items():
            origConfig[var] = p4PythonObj.__getattribute__(var)
            p4PythonObj.__setattr__(var, value)
            self._logDebug("overriding p4Config['%s'] = %s with %s"
                           % (var, str(origConfig[var]), str(value)))

# TODO ping server before each command?
        self._logDebug("Executing:", p4SubCmd, listArgs)
        p4Out = p4PythonObj.run(p4SubCmd, listArgs)
        self._logDebug("p4Out: ", p4Out)

        # restore p4Python settings changed for this command only
        for var in p4Config:
            p4PythonObj.__setattr__(var, origConfig[var])
            self._logDebug("resetting p4Config['%s'] = %s"
                           % (var, str(origConfig[var])))

# TODO Should do something to detect disconnects, etc.

        # If we have errors and warnings, we want to give both to caller
        if len(p4PythonObj.errors) > 0:
            errMsg = "ERROR: " + "".join(p4PythonObj.errors)

            if len(p4PythonObj.warnings) > 0:
                errMsg += "\nWARNING: " + "".join(p4PythonObj.warnings)

            raise P4Fatal("P4 Command Failed:\n" + errMsg)

        if len(p4PythonObj.warnings) > 0:
            warnMsg = "WARNING: " + "".join(p4PythonObj.warnings)
            raise P4Warning("P4 Command Warned:\n" + warnMsg)

        return p4Out

    def _connect(self):
        p4PythonObj = self._getAttr('p4PythonObj')

        if p4PythonObj is None:
            p4PythonObj = P4()
            try:
                p4PythonObj.connect()
                p4PythonObj.exception_level = 0
            except P4Exception as exc:
                raise P4Fatal("P4 Connection Failed") from exc

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
        configFile = os.path.dirname(__file__) + "/p4Config.yml"

        self._p4PythonSchema = _P4OOP4PythonSchema(configFile=configFile)
        return True

    def __del__(self):
        self._disconnect()
        return True
