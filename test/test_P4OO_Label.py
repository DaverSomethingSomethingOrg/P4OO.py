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
import P4OO._Exceptions
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
    assert allLabels.listObjectIDs() == []
    
    p4l1 = P4OO.Label.P4OOLabel(p4PythonObj=p4PythonObj, id="P4-OO-0.00_01")
    assert isinstance(p4l1, P4OO.Label.P4OOLabel)
    assert isinstance(p4l1, P4OO._SpecObj._P4OOSpecObj)

    import pprint
    
    # Label doesn't exist
    with pytest.raises(P4.P4Exception):
        pprint.pprint(id(p4l1.getLastChange()))

    p4l2 = P4OO.Label.P4OOLabel(p4PythonObj=p4PythonObj, id="P4-OO-0.00_02")
    with pytest.raises(P4.P4Exception):
        pprint.pprint(p4l2.getLastChange()._getSpecID())

    p4cl1 = P4OO.Client.P4OOClient(p4PythonObj=p4PythonObj, id="Davids-MacBook-Air")

    # Changes from p4l1 to p4l2 using client p4cl1
    with pytest.raises(P4.P4Exception):
        pprint.pprint(p4l1.getChangesFromLabels(p4l2, p4cl1))

    pprint.pprint(p4cl1.getOpenedFiles())

    with pytest.raises(P4.P4Exception):
        pprint.pprint(p4l1.getDiffsFromLabels(p4l2, p4cl1))
