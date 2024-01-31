#!/usr/bin/env python3

######################################################################
#  Copyright (c)2015,2024 David L. Armstrong
#
#  test/P4OO/Counter.py
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
import unittest

# _P4GoldenEgg is used for our test environment setup and destruction
import tempfile
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
testEgg = "./_P4GoldenEggs/P4OOCounter.tar.gz"
tmpDir = "./tmp"
p4PythonObj = None
p4Port = None
p4RootDir = None


######################################################################
# Class Initialization
#
class TestP4OO_Counter(unittest.TestCase):

    def test_construction(self):
        ''' Construct a P4OOCounter object and make sure its type checks out.'''

        testObj1 = P4OO.Counter.P4OOCounter()
        self.assertTrue(isinstance(testObj1, P4OO.Counter.P4OOCounter))
        self.assertTrue(isinstance(testObj1, P4OO._Base._P4OOBase))
#p4c1 = P4OOChange(p4PythonObj=p4PythonObj)

    def test_getValue(self):
        # Get a counter from the Egg and verify its value is what we expect
        testObj1 = P4OOCounter(id="change", p4PythonObj=p4PythonObj)
        self.assertEqual(testObj1.getValue(), 0,
                         'change counter value is 0')

        testObj2 = P4OOCounter(id="newcounter", p4PythonObj=p4PythonObj)
        self.assertEqual(testObj2.getValue(), 0,
                         'non-existant counter value is 0')

        self.assertEqual(testObj2.setValue(31337), 31337,
                         'setting non-existant counter value to 31337 returns 31337')

        self.assertEqual(testObj2.getValue(), 31337,
                         'new counter value is 31337')


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
