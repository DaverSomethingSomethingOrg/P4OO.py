#!/usr/bin/env python3

######################################################################
#  Copyright (c)2024 David L. Armstrong
#
#  test/test_P4OO_Label.py
#
######################################################################

#NAME / DESCRIPTION
'''
unittest test suite for P4OO.Label
'''

######################################################################
# Includes
#
import os  # used for managing environment variables
import pwd
import pytest

# _P4GoldenEgg is used for our test environment setup and destruction
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4
import P4OO.Label
import P4OO.Client
import P4OO._SpecObj


######################################################################
# Configuration
#
p4d = "p4d"
testEgg = "_P4GoldenEggs/P4OOLabel.tar.gz"
p4PythonObj = None
p4Port = None
p4RootDir = None


######################################################################
# Test Environment Initialization and Clean up
#
@pytest.fixture()
def p4PythonObj(tmp_path_factory, shared_datadir):
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

    yield p4PythonObj


def test_basic(p4PythonObj):

    allLabels = P4OO.Label.P4OOLabelSet(p4PythonObj=p4PythonObj).query()
    assert allLabels.listObjectIDs() == ['emptyLabel', 'initialLabel', 'secondLabel']
    
    p4l0 = P4OO.Label.P4OOLabel(p4PythonObj=p4PythonObj, id="emptyLabel")
    assert isinstance(p4l0, P4OO.Label.P4OOLabel)
    assert isinstance(p4l0, P4OO._SpecObj._P4OOSpecObj)

    # emptyLabel has no changes
    assert p4l0.getLastChange() is None

    p4l1 = P4OO.Label.P4OOLabel(p4PythonObj=p4PythonObj, id="initialLabel")
    
    # initialLabel is on Change 1
    lastChange = p4l1.getLastChange()
    assert lastChange is not None
    assert lastChange._getSpecID() == 1

    # secondLabel is on Change 3
    p4l2 = P4OO.Label.P4OOLabel(p4PythonObj=p4PythonObj, id="secondLabel")
    assert p4l2.getLastChange()._getSpecID() == 3

    p4cl1 = P4OO.Client.P4OOClient(p4PythonObj=p4PythonObj, id="clientDoesntExist")

    # Changes from p4l1 to p4l2 using client p4cl1 - default client viewspec is everything
    assert p4l1.getChangesFromLabels(p4l2, p4cl1).listObjectIDs() == [3, 2]

    assert p4l1.getDiffsFromLabels(p4l2, p4cl1) == ['==== //depot/testFile1#1 (text) - //depot/testFile1#2 (text) ==== content',
                                                    '1c1\n< test file 1 content\n---\n> test file 1 replaced content\n',
                                                    '',
                                                    '==== //depot/testFile2#1 (text) - //depot/testFile2#2 (text) ==== content',
                                                    '1a2\n> test file 2 updated content\n',
                                                    '',
                                                   ]

#TODO test creating new labels and tagging client files into label