#!/usr/bin/env python3

######################################################################
#  Copyright (c)2024 David L. Armstrong
#  Copyright (c)2013 David L. Armstrong, Cisco Systems, Inc.
#
#  test/test_P4OO__P4Python.py
#
######################################################################

#NAME / DESCRIPTION
'''
unittest test suite for _P4Python
'''

######################################################################
# Includes
#
import os  # used for managing environment variables
from pathlib import PosixPath

# P4OO._Base brings in our Exception hierarchy
import P4OO._Base
import pytest

# _P4GoldenEgg is used for our test environment setup and destruction
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4

# We might just need these yo
import P4OO._P4Python,P4OO._Connection


######################################################################
# Configuration
#
p4d = "p4d"
testEgg = "_P4GoldenEggs/_P4Python.tar.gz"
p4Port = None
p4RootDir = None


@pytest.fixture()
def p4PythonObj(tmp_path_factory, shared_datadir):
    # sanitize P4 environment variables
    for p4Var in ('P4CONFIG', 'P4PORT', 'P4USER', 'P4CLIENT'):
        if p4Var in os.environ:
            del(os.environ[p4Var])

    global testEgg, p4RootDir, p4d, p4Port
    p4RootDir = tmp_path_factory.mktemp("p4Root")
    eggDir = _P4GoldenEgg.eggTarball(shared_datadir / testEgg).unpack(p4RootDir)
    p4Port = eggDir.getP4Port(p4d=p4d)

    # Connect to the Perforce Service
    p4PythonObj = P4.P4()
    p4PythonObj.port = p4Port
#    assert p4Port == 1
    p4PythonObj.connect()
    
    return p4PythonObj


def test_construction(p4PythonObj):
    testObj1 = P4OO._P4Python._P4OOP4Python()
    assert isinstance(testObj1, P4OO._P4Python._P4OOP4Python)
    assert isinstance(testObj1, P4OO._Connection._P4OOConnection)
#p4c1 = P4OOChange(p4PythonObj=p4PythonObj)


def test_connectDisconnect(p4PythonObj):
    # test connection using our global p4PythonObj
    testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)
    testP4PythonObj = testObj1._connect()

    # not getting back p4 connection injected dependency
    assert testP4PythonObj == p4PythonObj

    # _disconnect() should always return True
    assert testObj1._disconnect()

    # dependency injected p4python object should not be disconnected
    assert testP4PythonObj.connected()

    # Should still return True, even if disconnected
    assert testObj1._disconnect()

    # Now use the same global P4PORT but have the test object instantiate a new connection
    os.environ['P4PORT'] = p4Port
    testP4PythonObj = testObj1._connect()

    # should be equivalent, but distinct connection objects
    assert testP4PythonObj != p4PythonObj

    # _disconnect() should always return True
    assert testObj1._disconnect()

    # Since the connection object was "owned" by the test object, it should be disconnected now too.
    assert not testP4PythonObj.connected()


def test_destructor(p4PythonObj):
    # Basically testing disconnect

    # test destruction using our global p4PythonObj
    testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)
    testObj1 = None

    # Since we injected the connection, it should still be connected.
    assert p4PythonObj.connected()

    # Now use the same global P4PORT but have the test object instantiate a new connection
    os.environ['P4PORT'] = p4Port

    testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)
    testP4PythonObj = testObj1._connect()
    testObj1 = None

    # Since we injected the connection, it should still be connected.
    assert testP4PythonObj.connected()


def test__initialize(p4PythonObj):

#    # _P4PYTHON_COMMAND_TRANSLATION should be "None" before _initialize()
#    assert P4OO._P4Python._P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION is None

    testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)

    # _initialize() should always return True
    assert testObj1._initialize()

    # We won't check the content, we don't care as long as comamnds work
    # _P4PYTHON_COMMAND_TRANSLATION should be dict after _initialize()
    assert isinstance(P4OO._P4Python._P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION, dict)


def test__execCmd(p4PythonObj):
    testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)

    # test with 0 args
    p4Out = testObj1._execCmd("info")

    # _execCmd("info") should return list
    assert isinstance(p4Out, list)

    # _execCmd("info") should be list length 1
    assert len(p4Out) == 1

    # "info" p4Out[0] should be a dict
    assert isinstance(p4Out[0], dict)

    global p4RootDir

    # info["serverRoot"] should be our test environment (p4RootDir)
    assert PosixPath(p4Out[0]['serverRoot']) == p4RootDir

    # test with multiple args for default spec values
    p4Out = testObj1._execCmd("user", "-o", "testuser")

    # "user -o testuser" p4Out[0] should be a dict
    assert isinstance(p4Out[0], dict)

    # test with last arg empty... P4Python doesn't like this normally
    p4Out = testObj1._execCmd("user", "-o", "testuser", "")
    # "user -o testuser \'\'" p4Out[0] should be a dict
    assert isinstance(p4Out[0], dict)

    # test with multiple args for spec that won't and will not have defaults
    def exceptCallable(*args, **kwargs):
        testObj1._execCmd("change", "-o", 99999)
#    self.assertRaises(P4.P4Exception, exceptCallable,
#                      '"change -o 99999" should raise P4.P4Exception')

    # test p4Port override on connected object
    #   P4.P4Exception: Can't change port once you've connected.
    def exceptCallable(*args, **kwargs):
        testObj1._execCmd("info", port=p4Port)
#    self.assertRaises(P4.P4Exception, exceptCallable,
#                      '_execCmd overriding P4PORT on connected object should raise P4.P4Exception')

    # test p4Port override on new/unconnected object
    p4Out = testObj1._execCmd("user", "-o", user="testUser")
    # _execCmd overriding P4USER for "user -o" should return overridden userid
    assert p4Out[0]["User"] == "testUser"


def test__parseOutput(p4PythonObj):
#    testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)

    # test user spec parsing
#    p4Out = testObj1._execCmd("users")
#        print(p4Out)
#    parsedOutput = testObj1._parseOutput("users", p4Out)
#        print(parsedOutput)
    pass

def test_refreshSpec(p4PythonObj):
    pass

def test_readSpec(p4PythonObj):
    pass

def test_runCommand(p4PythonObj):
    pass

#TODO readSpec and saveSpec are pretty important.  Modularity says test them here somehow

