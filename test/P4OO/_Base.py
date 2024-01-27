#!/usr/bin/env python3.2

######################################################################
#  Copyright (c)2011-2012, David L. Armstrong.
#
#  test/P4OO._Base.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce _Base unittest Class

'''

######################################################################
# Include Paths
#
import sys
sys.path.append('../lib')


######################################################################
# Includes
#
# P4OO._Base brings in our Exception hierarchy
import P4OO._Base
import unittest

######################################################################
# P4Python Class Initialization
#


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
        testObj1 = P4OO._Base._P4OOBase()
        self.assertTrue(isinstance(testObj1, P4OO._Base._P4OOBase))
        self.assertEqual(testObj1._getAttr("foo"), None, "_getAttr for non-existing attribute returns None")
        self.assertEqual(testObj1._getAttr("foo"), None, "subsequent _getAttr for non-existing attribute also returns None")
        self.assertEqual(testObj1._setAttr("foo", "bar"), "bar", "_setAttr for new attribute returns value")
        self.assertEqual(testObj1._getAttr("foo"), "bar", "_getAttr for existing attribute returns value")
        self.assertEqual(testObj1._setAttr("foo", "baz"), "baz", "_setAttr for existing attribute returns value")
        self.assertEqual(testObj1._getAttr("foo"), "baz", "_getAttr for changed attribute returns new value")
        self.assertEqual(testObj1._delAttr("foo"), "baz", "_delAttr returns value of attribute")
        self.assertEqual(testObj1._getAttr("foo"), None, "_getAttr for non-existing attribute returns None")
        self.assertEqual(testObj1._delAttr("foo"), None, "_delAttr returns nothing for non-existant attribute")

    def test_init1Attr(self):
        testObj1 = P4OO._Base._P4OOBase(foo="bar")
        self.assertTrue(isinstance(testObj1, P4OO._Base._P4OOBase))
        self.assertEqual(testObj1._getAttr("foo"), "bar", "_getAttr for existing attribute returns value")
        self.assertEqual(testObj1._setAttr("foo", "baz"), "baz", "_setAttr for existing attribute returns value")
        self.assertEqual(testObj1._getAttr("foo"), "baz", "_getAttr for changed attribute returns new value")

    def test_basicMethods(self):
        testObj1 = P4OO._Base._P4OOBase()
        self.assertEqual(testObj1._uniqueID(), id(testObj1), "default _uniqueID returns id() value")
        self.assertEqual(testObj1._initialize(), 1, "default _initialize returns 1")


#    def test_Exceptions(self):
#        pass

#    def test_P4Connection(self):
#        pass

if __name__ == '__main__':
    unittest.main()


######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2011-2012, David L. Armstrong.
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
