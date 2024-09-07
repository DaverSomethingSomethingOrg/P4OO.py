#!/usr/bin/env python3

######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong
#
#  test/P4OO._Base.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce _Base unittest Class

'''

######################################################################
# Includes
#
import unittest
from dataclasses import dataclass, field

# P4OO._Base brings in our Exception hierarchy
import P4OO._Base

@dataclass
class testBase(P4OO._Base._P4OOBase):
    foo: str = field(default=None)

#class TestSequenceFunctions(unittest.TestCase):
class TestP4OO_Base(unittest.TestCase):
    def setUp(self):
#        self.seq = range(10)
        pass

    def tearDown(self):
#        self.widget.dispose()
#        self.widget = None
        pass

    # Test an object instantiated with no attributes
    def test_initEmpty(self):
#        testObj1 = P4OO._Base._P4OOBase()
        testObj1 = testBase()
        self.assertTrue(isinstance(testObj1, P4OO._Base._P4OOBase))
        self.assertEqual(testObj1.foo, None, "default value is None")
        testObj1.foo="bar"
        self.assertEqual(testObj1.foo, "bar", "mutable attribute set to new value")
        testObj1.foo="baz"
        self.assertEqual(testObj1.foo, "baz", "mutable attribute reset to new value")

    def test_init1Attr(self):
        testObj1 = testBase(foo="bar")
        self.assertTrue(isinstance(testObj1, P4OO._Base._P4OOBase))
        self.assertEqual(testObj1.foo, "bar", "non-default attribute returns expected value")
        testObj1.foo="baz"
        self.assertEqual(testObj1.foo, "baz", "mutable attribute set to new value")

    def test_basicMethods(self):
        testObj1 = testBase()
        self.assertEqual(testObj1._uniqueID(), id(testObj1), "default _uniqueID returns id() value")
        self.assertEqual(testObj1._initialize(), 1, "default _initialize returns 1")


#    def test_Exceptions(self):
#        pass

#    def test_P4Connection(self):
#        pass

if __name__ == '__main__':
    unittest.main()