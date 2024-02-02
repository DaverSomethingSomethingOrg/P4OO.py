#!/usr/bin/env python3

######################################################################
#  Copyright (c)2024 David L. Armstrong
#
#  test/test_P4OO_Client.py
#
######################################################################

#NAME / DESCRIPTION
'''
unittest test suite for P4OO.Client
'''

######################################################################
# Includes
#
import os  # used for managing environment variables
import pytest

# _P4GoldenEgg is used for our test environment setup and destruction
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4
import P4OO._Exceptions
import P4OO.Client
import P4OO._SpecObj


######################################################################
# Configuration
#
p4d = "p4d"
testEgg = "_P4GoldenEggs/P4OOClient.tar.gz"
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


def test_construction(initializeTests):
    testObj1 = P4OO.Client.P4OOClient()
    assert isinstance(testObj1, P4OO.Client.P4OOClient)
    assert isinstance(testObj1, P4OO._SpecObj._P4OOSpecObj)
