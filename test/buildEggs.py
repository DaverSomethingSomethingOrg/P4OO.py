#!/usr/bin/env python3

######################################################################
#  Copyright (c)2013, Cisco Systems, Inc.
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
import sys # used her for include path mgmt
sys.path.append('.')
sys.path.append('../lib')

# _P4GoldenEgg is used for our test environment setup and destruction
import tempfile
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4

# We might just need these yo
import P4OO._P4Python,P4OO._Connection
from P4OO.User import P4OOUser


######################################################################
# Configuration
#
p4d = "/export/disk2/tools/perforce-v10.2/bin.linux26x86_64/p4d"
testEggsDir = "./_P4GoldenEggs"
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
    p4PythonObj.connect()

    user1Obj = P4OOUser(p4PythonObj=p4PythonObj)
    user1Obj._setSpecAttr("User", "testUser1")
    user1Obj.saveSpec(force=True)

    user2Obj = P4OOUser(p4PythonObj=p4PythonObj)
    user2Obj._setSpecAttr("User", "testUser2")
    user2Obj.saveSpec(force=True)

    # Wrap it up and clean it up
    testEggTarball = testEggDir.createTarball(testEggsDir + "/_P4Python.tar.gz")
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
