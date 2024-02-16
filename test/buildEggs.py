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
import os
import os.path

# _P4GoldenEgg is used for our test environment setup and destruction
import tempfile
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4
from P4OO.User import P4OOUser
from P4OO.Client import P4OOClient
from P4OO.Label import P4OOLabel


######################################################################
# Configuration
#
p4d = "p4d"
testEggsDataDir = "./data/_P4GoldenEggs"
tmpDir = "./tmp"

# _P4Python.tar.gz
def createEgg__P4Python():

    global p4d, testEggsDataDir, tmpDir

    # Set up P4ROOT and configure a new EggDir to use it
    p4RootDir = os.path.abspath(tempfile.mkdtemp(dir=tmpDir))
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
    testEggDir.createTarball(testEggsDataDir + "/_P4Python.tar.gz")
    testEggDir.destroy()


# Client.tar.gz
def createEgg_Client():

    global p4d, testEggsDataDir, tmpDir

    # Set up P4ROOT and configure a new EggDir to use it
    p4RootDir = os.path.abspath(tempfile.mkdtemp(dir=tmpDir))
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
    testEggDir.createTarball(testEggsDataDir + "/P4OOClient.tar.gz")
    testEggDir.destroy()


def createEgg_Label():

    global p4d, testEggsDataDir, tmpDir

    # We'll derive the Label egg from Client egg
    testEgg = "P4OOClient.tar.gz"

    # Set up P4ROOT and configure a new EggDir to use it
    p4RootDir = os.path.abspath(tempfile.mkdtemp(dir=tmpDir))
    testEggDir = _P4GoldenEgg.eggTarball(testEggsDataDir + "/" + testEgg).unpack(p4RootDir)

    # Connect to the Perforce Service
    p4PythonObj = P4.P4()
    p4PythonObj.port = testEggDir.getP4Port(p4d=p4d)
    p4PythonObj.user = 'testEggCreator'
    p4PythonObj.connect()

    # Create a label pointing to nothing
    p4l0 = P4OOLabel(p4PythonObj=p4PythonObj, id="emptyLabel")
    p4l0.saveSpec()

    # Create 'testClient1' Workspace and our test files
    p4ClientRoot = os.path.abspath(tempfile.mkdtemp(dir=tmpDir))
    p4cl1 = P4OOClient(p4PythonObj=p4PythonObj, id="testClient1", root=p4ClientRoot)
    p4cl1._setSpecAttr("root", p4ClientRoot)
    p4cl1.saveSpec()

    '''
    [luser@329dec3cc399 P4OO.py]$ p4 print //depot/...@1
    //depot/testFile1#1 - add change 1 (text)
    test file 1 content
    //depot/testFile2#1 - add change 1 (text)
    test file 2 content
    '''
    testfile1Path = os.path.abspath(p4ClientRoot + "/" + "testFile1")
    with open(file=testfile1Path, mode="w", encoding="utf-8") as stream:
        print('test file 1 content', file=stream)

    testfile2Path = os.path.abspath(p4ClientRoot + "/" + "testFile2")
    with open(file=testfile2Path, mode="w", encoding="utf-8") as stream:
        print('test file 2 content', file=stream)

    p4Output = p4cl1.addFiles(testfile1Path, testfile2Path)

    import pprint
#    pprint.pprint(p4Output)

#    pprint.pprint(p4cl1.getOpenedFiles())

    ''' Change 1 on 2024/02/03 by testUser1@testClient1 'initial change' '''
    p4Output = p4cl1.submitChange(description="initial change")
#    pprint.pprint(p4Output)

    # No more opened files
#    pprint.pprint(p4cl1.getOpenedFiles())

    # 'initial change\n'
#    pprint.pprint(P4OOChangeSet(p4PythonObj=p4PythonObj).query()[0]._getSpecAttr('description'))

    ''' Label initialLabel 2024/02/03 'Created by testUser1. ' '''
    p4l1 = P4OOLabel(p4PythonObj=p4PythonObj, id="initialLabel")
    p4l1.saveSpec()
    pprint.pprint(p4l1.tagFiles(testfile1Path, testfile2Path, p4client=p4cl1))
#    pprint.pprint(p4l1.getDiffsFromLabels(otherLabel=p4l0, client=p4cl1))


    '''
    [luser@329dec3cc399 P4OO.py]$ p4 print //depot/...@2
    //depot/testFile1#1 - add change 1 (text)
    test file 1 content
    //depot/testFile2#2 - edit change 2 (text)
    test file 2 content
    test file 2 updated content
    '''
    p4Output = p4cl1.editFiles(testfile2Path)
#    pprint.pprint(p4Output)

    with open(file=testfile2Path, mode="a", encoding="utf-8") as stream:
        print('test file 2 updated content', file=stream)

#    pprint.pprint(p4cl1.getOpenedFiles())

    ''' Change 2 on 2024/02/03 by testUser1@testClient1 'update testFile2' '''
    p4Output = p4cl1.submitChange(description="update testFile2")
#    pprint.pprint(p4Output)


    '''
    [luser@329dec3cc399 P4OO.py]$ p4 print //depot/...@3
    //depot/testFile1#2 - edit change 3 (text)
    test file 1 replaced content
    //depot/testFile2#2 - edit change 2 (text)
    test file 2 content
    test file 2 updated content
    [luser@329dec3cc399 P4OO.py]$ 
    '''
    p4Output = p4cl1.editFiles(testfile1Path)
#    pprint.pprint(p4Output)

    with open(file=testfile1Path, mode="w", encoding="utf-8") as stream:
        print('test file 1 replaced content', file=stream)

#    pprint.pprint(p4cl1.getOpenedFiles())


    ''' Change 3 on 2024/02/03 by testUser1@testClient1 'update testFile1' '''
    p4Output = p4cl1.submitChange(description="update testFile1")
#    pprint.pprint(p4Output)

    p4l2 = P4OOLabel(p4PythonObj=p4PythonObj, id="secondLabel")
    p4l2.saveSpec()
    pprint.pprint(p4l2.tagFiles(testfile1Path, testfile2Path, p4client=p4cl1))
#    pprint.pprint(p4l2.getDiffsFromLabels(otherLabel=p4l1, client=p4cl1))

#    pprint.pprint(p4l1.getChangesFromLabels(otherLabel=p4l2, client=p4cl1))

    # Wrap it up and clean it up
    testEggDir.createTarball(testEggsDataDir + "/P4OOLabel.tar.gz")
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
    createEgg_Label()
