#!/usr/bin/env python3

######################################################################
#  Copyright (c)2024 David L. Armstrong
#  Copyright (c)2013 Cisco Systems, Inc.
#
#  test/buildEggs.py
#
######################################################################

#NAME / DESCRIPTION
'''
P4OO.Py test helper script to rebuild all Golden Egg tarballs to expected
state.  Useful for migrating Eggs to different versions of Perforce.

This depends on having a working P4OO installation, so be sure to avoid
Chicken and Egg issues trying to test P4OO on a new platform.
'''

######################################################################
# Includes
#
import os  # used for managing environment variables

# _P4GoldenEgg is used for our test environment setup and destruction
import tempfile
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4
from P4OO.User import P4OOUser
from P4OO.Client import P4OOClient


######################################################################
# Configuration
#
p4d = "p4d"
testEggsDir = "./data/_P4GoldenEggs"
tmpDir = "./tmp"


# _P4Python.tar.gz
def createEgg__P4Python():

    global p4d, testEggsDir, tmpDir

    # Set up P4ROOT and configure a new EggDir to use it
    p4RootDir = tempfile.mkdtemp(dir=tmpDir)
    testEggDir = _P4GoldenEgg.eggDirectory(p4RootDir)

    # Connect to the Perforce Service
    p4PythonObj = P4.P4()
    p4PythonObj.port = testEggDir.getP4Port(p4d=p4d)
    # The user creating the objects gets added by default
    p4PythonObj.user = 'testEggCreator'
    p4PythonObj.connect()

    user1Obj = P4OOUser(p4PythonObj=p4PythonObj)
    user1Obj._setSpecAttr("User", "testUser1")
    user1Obj.saveSpec(force=True)

    user2Obj = P4OOUser(p4PythonObj=p4PythonObj)
    user2Obj._setSpecAttr("User", "testUser2")
    user2Obj.saveSpec(force=True)

    # Wrap it up and clean it up
    testEggDir.createTarball(testEggsDir + "/_P4Python.tar.gz")
    testEggDir.destroy()


# Client.tar.gz
def createEgg_Client():

    global p4d, testEggsDir, tmpDir

    # Set up P4ROOT and configure a new EggDir to use it
    p4RootDir = tempfile.mkdtemp(dir=tmpDir)
    testEggDir = _P4GoldenEgg.eggDirectory(p4RootDir)

    # Connect to the Perforce Service
    p4PythonObj = P4.P4()
    p4PythonObj.port = testEggDir.getP4Port(p4d=p4d)
    p4PythonObj.user = 'testEggCreator'
    p4PythonObj.connect()

    user1Obj = P4OOUser(p4PythonObj=p4PythonObj)
    user1Obj._setSpecAttr("User", "testUser1")
    user1Obj.saveSpec(force=True)

    user2Obj = P4OOUser(p4PythonObj=p4PythonObj)
    user2Obj._setSpecAttr("User", "testUser2")
    user2Obj.saveSpec(force=True)

    # Wrap it up and clean it up
    testEggDir.createTarball(testEggsDir + "/Client.tar.gz")
    testEggDir.destroy()


######################################################################
# MAIN
#
if __name__ == '__main__':
    # sanitize P4 environment variables
    for p4Var in ('P4CONFIG', 'P4PORT', 'P4USER', 'P4CLIENT'):
        if p4Var in os.environ:
            del(os.environ[p4Var])

    createEgg__P4Python()
    createEgg_Client()
