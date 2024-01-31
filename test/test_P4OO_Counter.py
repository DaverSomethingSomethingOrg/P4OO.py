#!/usr/bin/env python3

######################################################################
#  Copyright (c)2015,2024 David L. Armstrong
#
#  test/test_P4OO_Counter.py
#
######################################################################

#NAME / DESCRIPTION
'''
unittest test suite for P4OO.Counter
'''

######################################################################
# Includes
#
import os  # used for managing environment variables

# P4OO._Base brings in our Exception hierarchy
import P4OO._Base
import pytest

# _P4GoldenEgg is used for our test environment setup and destruction
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4

# We might just need these yo
import P4OO.Counter
from P4OO.Counter import P4OOCounter, P4OOCounterSet


######################################################################
# Configuration
#
p4d = "p4d"
testEgg = "_P4GoldenEggs/P4OOCounter.tar.gz"
p4PythonObj = None
p4Port = None
p4RootDir = None

######################################################################
# Test Environment Initialization and Clean up
#
@pytest.fixture()
def initializeTests(tmp_path_factory, shared_datadir):
    # sanitize P4 environment variables
    for p4Var in ('P4CONFIG', 'P4PORT', 'P4USER', 'P4CLIENT'):
        if p4Var in os.environ:
            del(os.environ[p4Var])

    global testEgg, p4RootDir, p4d, p4PythonObj, p4Port
    p4RootDir = tmp_path_factory.mktemp("p4Root")
    eggDir = _P4GoldenEgg.eggTarball(shared_datadir / testEgg).unpack(p4RootDir)
    p4Port = eggDir.getP4Port(p4d=p4d)

    # Connect to the Perforce Service
    p4PythonObj = P4.P4()
    p4PythonObj.port = p4Port
    p4PythonObj.connect()

    return p4RootDir

def test_construction(initializeTests):
    ''' Construct a P4OOCounter object and make sure its type checks out.'''

    testObj1 = P4OO.Counter.P4OOCounter()
    assert isinstance(testObj1, P4OO.Counter.P4OOCounter)
    assert isinstance(testObj1, P4OO._Base._P4OOBase)


def test_getValue(initializeTests):
    ''' Get a counter from the Egg and verify its value is what we expect '''
    
    changeCounter = P4OOCounter(id="change", p4PythonObj=p4PythonObj)
    assert changeCounter.getValue() == 0

    nonExistantCounter = P4OOCounter(id="newcounter", p4PythonObj=p4PythonObj)
    assert nonExistantCounter.getValue() == 0
    assert nonExistantCounter.setValue(31337) == 31337
    assert nonExistantCounter.getValue() == 31337
