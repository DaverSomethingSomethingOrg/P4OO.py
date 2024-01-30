#!/usr/bin/env python3.2

######################################################################
#  Copyright (c)2013, Cisco Systems, Inc.
#
#  test/P4OO/_P4Python.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
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
import sys # used her for include path mgmt
sys.path.append('.')
sys.path.append('../lib')

# P4OO._Base brings in our Exception hierarchy
import P4OO._Base
import unittest

# _P4GoldenEgg is used for our test environment setup and destruction
import tempfile
import _P4GoldenEgg

# We use dependency injection with P4 for our tests
import P4

# We might just need these yo
import P4OO._P4Python,P4OO._Connection


######################################################################
# Configuration
#
p4d = "/export/disk2/tools/perforce-v10.2/bin.linux26x86_64/p4d"
testEgg = "./_P4GoldenEggs/_P4Python.tar.gz"
tmpDir = "./tmp"
p4PythonObj = None
p4Port = None
p4RootDir = None


######################################################################
# Class Initialization
#
class TestP4OO_P4Python(unittest.TestCase):

    def test_construction(self):
        testObj1 = P4OO._P4Python._P4OOP4Python()
        self.assertTrue(isinstance(testObj1, P4OO._P4Python._P4OOP4Python))
        self.assertTrue(isinstance(testObj1, P4OO._Connection._P4OOConnection))
#p4c1 = P4OOChange(p4PythonObj=p4PythonObj)


    def test_connectDisconnect(self):
        # test connection using our global p4PythonObj
        testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)
        testP4PythonObj = testObj1._connect()
        self.assertEqual(testP4PythonObj, p4PythonObj,
                         'not getting back p4 connection injected dependency')

        self.assertEqual(testObj1._disconnect(), True,
                         '_disconnect() should always return True')

        # Since we injected the connection, it should still be connected.
        self.assertEqual(testP4PythonObj.connected(), True,
                         'dependency injected p4python object should not be disconnected')


        # Should still return True, even if disconnected
        self.assertEqual(testObj1._disconnect(), True,
                         '_disconnect() should always return True')

        # Now use the same global P4PORT but have the test object instantiate a new connection
        os.environ['P4PORT'] = p4Port
        testP4PythonObj = testObj1._connect()

        # should be equivalent, but distinct connection objects
        self.assertNotEqual(testP4PythonObj, p4PythonObj,
                         'not getting back new p4 connection object after disconnect')

        self.assertEqual(testObj1._disconnect(), True,
                         '_disconnect() should always return True')

        # Since the connection object was "owned" by the test object, it should be disconnected now too.
        self.assertEqual(testP4PythonObj.connected(), False,
                         'owned p4python object should be disconnected')


    def test_destructor(self):
        # Basically testing disconnect

        # test destruction using our global p4PythonObj
        testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)
        testObj1 = None

        # Since we injected the connection, it should still be connected.
        self.assertEqual(p4PythonObj.connected(), True,
                         'dependency injected p4python object should not be disconnected at destruction')

        # Now use the same global P4PORT but have the test object instantiate a new connection
        os.environ['P4PORT'] = p4Port

        testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)
        testP4PythonObj = testObj1._connect()
        testObj1 = None

        # Since we injected the connection, it should still be connected.
        self.assertEqual(testP4PythonObj.connected(), True,
                         'owned p4python object should be disconnected at destruction')


    def test__initialize(self):
        self.assertEqual(P4OO._P4Python._P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION, None,
                         '_P4PYTHON_COMMAND_TRANSLATION should be "None" before _initialize()')

        testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)

        self.assertEqual(testObj1._initialize(), True,
                         '_initialize() should always return True')

        # We won't check the content, we don't care as long as comamnds work
        self.assertIsInstance(P4OO._P4Python._P4OOP4Python._P4PYTHON_COMMAND_TRANSLATION, dict,
                         '_P4PYTHON_COMMAND_TRANSLATION should be dict after _initialize()')


    def test__execCmd(self):
        testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)

        # test with 0 args
        p4Out = testObj1._execCmd("info")
        self.assertIsInstance(p4Out, list,
                         '_execCmd("info" didn\'t return list')
        self.assertEqual(len(p4Out), 1,
                         '_execCmd("info" didn\'t return list length 1')
        self.assertIsInstance(p4Out[0], dict,
                         '"info" p4Out[0] should be a dict')

        global p4RootDir
        self.assertEqual(p4Out[0]['serverRoot'], p4RootDir,
                         'info["serverRoot"] should be our test environment: ' + p4RootDir)

        # test with multiple args for default spec values
        p4Out = testObj1._execCmd("user", "-o", "testuser")
        self.assertIsInstance(p4Out[0], dict,
                         '"user -o testuser" p4Out[0] should be a dict')

        # test with last arg empty... P4Python doesn't like this normally
        p4Out = testObj1._execCmd("user", "-o", "testuser", "")
        self.assertIsInstance(p4Out[0], dict,
                         '"user -o testuser \'\'" p4Out[0] should be a dict')

        # test with multiple args for spec that won't and will not have defaults
        def exceptCallable(*args, **kwargs):
            testObj1._execCmd("change", "-o", 99999)
        self.assertRaises(P4.P4Exception, exceptCallable,
                          '"change -o 99999" should raise P4.P4Exception')

        # test p4Port override on connected object
        #   P4.P4Exception: Can't change port once you've connected.
        def exceptCallable(*args, **kwargs):
            testObj1._execCmd("info", port=p4Port)
        self.assertRaises(P4.P4Exception, exceptCallable,
                          '_execCmd overriding P4PORT on connected object should raise P4.P4Exception')

        # test p4Port override on new/unconnected object
        p4Out = testObj1._execCmd("user", "-o", user="testUser")
        self.assertEqual(p4Out[0]["User"], "testUser",
                         '_execCmd overriding P4USER for "user -o" should return overridden userid')


    def test__parseOutput(self):
        testObj1 = P4OO._P4Python._P4OOP4Python(p4PythonObj=p4PythonObj)

        # test user spec parsing
        p4Out = testObj1._execCmd("users")
#        print(p4Out)
        parsedOutput = testObj1._parseOutput("users", p4Out)
#        print(parsedOutput)


    def test_runCommand(self):
        pass

#TODO readSpec and saveSpec are pretty important.  Modularity says test them here somehow


######################################################################
# Test Environment Initialization and Clean up
#
def initializeTests():
    # sanitize P4 environment variables
    for p4Var in ('P4CONFIG', 'P4PORT', 'P4USER', 'P4CLIENT'):
        if p4Var in os.environ:
            del(os.environ[p4Var])

    global tmpDir, testEgg, p4RootDir, p4d, p4PythonObj, p4Port
    p4RootDir = tempfile.mkdtemp(dir=tmpDir)
    eggDir = _P4GoldenEgg.eggTarball(testEgg).unpack(p4RootDir)
    p4Port = eggDir.getP4Port(p4d=p4d)

    # Connect to the Perforce Service
    p4PythonObj = P4.P4()
    p4PythonObj.port = p4Port
    p4PythonObj.connect()


def cleanUpTests():
#TODO...
    # self.eggDir.destroy()
    # self._initialized = None
    pass

######################################################################
# MAIN
#
if __name__ == '__main__':
    initializeTests()
    unittest.main()
    cleanUpTests()


######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2013, Cisco Systems, Inc.
#
#   This module is distributed under the terms of the Artistic License
# 2.0.  For more details, see the full text of the license in the file
# LICENSE.
#
# SUPPORT AND WARRANTY
#
#   This program is distributed in the hope that it will be
# useful, but it is provided "as is" and without any expressed
# or implied warranties.
#
