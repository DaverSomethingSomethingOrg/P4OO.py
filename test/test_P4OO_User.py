#!/usr/bin/env python3

######################################################################
#  Copyright (c)2024 David L. Armstrong
#
#  test/test_P4OO_User.py
#
######################################################################

#NAME / DESCRIPTION
'''
unittest test suite for P4OO.User
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
import P4OO.User
import P4OO._SpecObj


######################################################################
# Configuration
#
p4d = "p4d"
testEgg = "_P4GoldenEggs/P4OOUser.tar.gz"
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

    allusers = P4OO.User.P4OOUserSet(p4PythonObj=p4PythonObj).query()
    assert allusers.listObjectIDs() == ['testEggCreator', 'testUser1', 'testUser2']
    
    testuser1Obj = P4OO.User.P4OOUser(p4PythonObj=p4PythonObj, id='testuser1')
    assert isinstance(testuser1Obj, P4OO.User.P4OOUser)
    assert isinstance(testuser1Obj, P4OO._SpecObj._P4OOSpecObj)

    # test default/detected spec id
    myP4UserObj = P4OO.User.P4OOUser(p4PythonObj=p4PythonObj)
    myPwUidUserId = pwd.getpwuid(os.getuid())[0]
    assert myP4UserObj._getSpecID() == myPwUidUserId

    # test __repr__
    assert myP4UserObj.__repr__() == f'P4OOUser({myPwUidUserId})'

    testNewUserObj = P4OO.User.P4OOUser(p4PythonObj=p4PythonObj, id='newUser')
    
    # cannot delete non-existant user if isn't current user
    with pytest.raises(P4.P4Exception):
        testNewUserObj.deleteSpec()

    # non-admin user cannot save a user other than self
    with pytest.raises(P4.P4Exception):
        testNewUserObj.saveSpec()

    allusers = P4OO.User.P4OOUserSet(p4PythonObj=p4PythonObj).query()
    assert allusers.listObjectIDs() == ['luser', 'testEggCreator', 'testUser1', 'testUser2']

    # Can delete own spec even if doesn't really exist in DB
    myP4UserObj.deleteSpec()
    allusers = P4OO.User.P4OOUserSet(p4PythonObj=p4PythonObj).query()
    assert allusers.listObjectIDs() == ['testEggCreator', 'testUser1', 'testUser2']

    # test saveSpec / refreshSpec
    myP4UserObj = P4OO.User.P4OOUser(p4PythonObj=p4PythonObj)
    assert myP4UserObj._setSpecAttr('email', 'newUser@testHost') == 'newUser@testHost'
    assert myP4UserObj._setSpecAttr('fullname', "New User") == "New User"

    assert myP4UserObj._getSpecAttr('email') == 'newUser@testHost'

    # Prior to saveSpec we have a modifiedSpec different from p4SpecObj
    # Trigger __initialize() first though.. we just "deleted" this thing
    assert myP4UserObj._getSpecID() == 'luser'
    assert myP4UserObj._getAttr('modifiedSpec')['fullname'] != myP4UserObj._getAttr('p4SpecObj')['FullName']
    
    assert myP4UserObj.saveSpec() == True
    
    # After saveSpec modifiedSpec must match p4SpecObj
    assert myP4UserObj._getAttr('modifiedSpec')['fullname'] == myP4UserObj._getAttr('p4SpecObj')['FullName']
    
    # test _getSpecAttr()
    assert myP4UserObj._getSpecAttr('email') == 'newUser@testHost'

    # test _delSpecAttr()
    assert myP4UserObj._delSpecAttr('email') == 'newUser@testHost'
    assert myP4UserObj._delSpecAttr('email') is None
    assert myP4UserObj._getAttr('modifiedSpec')['email'] != myP4UserObj._getAttr('p4SpecObj')['Email']

    # Spec is incomplete without Email field
    with pytest.raises(P4.P4Exception):
        assert myP4UserObj.saveSpec() == True

    allusers = P4OO.User.P4OOUserSet(p4PythonObj=p4PythonObj).query()
    assert allusers.listObjectIDs() == ['luser', 'testEggCreator', 'testUser1', 'testUser2']

    # At least run the code and make sure there aren't any exceptions
#TODO
    myP4UserObj._toJSON()

#TODO
    myP4UserObj.deleteWithVengeance()