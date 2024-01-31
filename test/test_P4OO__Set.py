#!/usr/bin/env python3

######################################################################
#  Copyright (c)2012,2024 David L. Armstrong
#
#  test/P4OO._Set.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce _Set unittest Class

'''

######################################################################
# Includes
#
# P4OO._Base brings in our Exception hierarchy
import P4OO._Set
import unittest

######################################################################
# P4Python Class Initialization
#


#class TestSequenceFunctions(unittest.TestCase):
class TestP4OO_Set(unittest.TestCase):
    def setUp(self):
#        self.seq = range(10)
        pass

    # Test an object instantiated with no attributes
    def test_BaseFunctionality(self):
        testObj1 = P4OO._Set._P4OOSet()
        self.assertTrue(isinstance(testObj1, P4OO._Set._P4OOSet))
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

    def test_setConstruction(self):
        testObj1 = P4OO._Set._P4OOSet(iterable=[1, 2, 3])
        self.assertTrue(isinstance(testObj1, P4OO._Set._P4OOSet))
        self.assertTrue(isinstance(testObj1, P4OO._OrderedSet.OrderedSet))
        self.assertTrue(isinstance(testObj1, P4OO._Base._P4OOBase))
        self.assertEqual(repr(testObj1), "_P4OOSet([1, 2, 3])", "repr() for set [1, 2, 3] returns '_P4OOSet([1, 2, 3])'")
        testObj2 = P4OO._Set._P4OOSet(iterable=testObj1)
        self.assertEqual(repr(testObj2), "_P4OOSet([1, 2, 3])", "copy constructor gives same repr()")
        testObj3 = P4OO._Set._P4OOSet(iterable=['a', 'b', 'c'])
        self.assertEqual(repr(testObj3), "_P4OOSet(['a', 'b', 'c'])", "repr() for set ['a', 'b', 'c'] returns '_P4OOSet(['a', 'b', 'c'])'")

    def test_setSetFunctionality(self):
        testObj1 = P4OO._Set._P4OOSet(iterable=[1, 2, 3])
        testObj2 = P4OO._Set._P4OOSet(iterable=[3, 4, 5])
        self.assertEqual(len(testObj1), 3, "len([1, 2, 3]) is 3")
        testObj3 = testObj1 & testObj2
        self.assertTrue(isinstance(testObj3, P4OO._Set._P4OOSet))
        self.assertEqual(repr(testObj3), "_P4OOSet([3])", "intersection: [1, 2, 3] & [3, 4, 5] == [3]")
        testObj4 = testObj1 | testObj2
        self.assertEqual(repr(testObj4), "_P4OOSet([1, 2, 3, 4, 5])", "union: [1, 2, 3] | [3, 4, 5] == [1, 2, 3, 4, 5]")
        self.assertEqual(len(testObj4), 5, "len([1, 2, 3, 4, 5]) is 5")
        testObj4.add(3)
        self.assertEqual(repr(testObj4), "_P4OOSet([1, 2, 3, 4, 5])", "add(3) to [1, 2, 3, 4, 5] stays the same")
        self.assertEqual(len(testObj4), 5, "len([1, 2, 3, 4, 5]) is 5")
        testObj4.add(6)
        self.assertEqual(repr(testObj4), "_P4OOSet([1, 2, 3, 4, 5, 6])", "add(6) to [1, 2, 3, 4, 5] makes [1, 2, 3, 4, 5, 6]")
        self.assertEqual(len(testObj4), 6, "len([1, 2, 3, 4, 5, 6]) is 6")
        testObj4.discard(0)
        self.assertEqual(repr(testObj4), "_P4OOSet([1, 2, 3, 4, 5, 6])", "discard(0) from [1, 2, 3, 4, 5, 6] stays the same")
        self.assertEqual(len(testObj4), 6, "len([1, 2, 3, 4, 5, 6]) is 6")
        testObj4.discard(6)
        self.assertEqual(repr(testObj4), "_P4OOSet([1, 2, 3, 4, 5])", "discard(6) from [1, 2, 3, 4, 5, 6] makes [1, 2, 3, 4, 5]")
        self.assertEqual(len(testObj4), 5, "len([1, 2, 3, 4, 5]) is 5")

    def test_setSetAddDel(self):
        testObj1 = P4OO._Set._P4OOSet(iterable=[1, 2, 3])
        testObj2 = P4OO._Set._P4OOSet(iterable=[3, 4, 5])
        testObj3 = P4OO._Set._P4OOSet(iterable=testObj1)  # copy the set, don't just assign
        testObj3.addObjects(testObj2)
        self.assertEqual(repr(testObj3), "_P4OOSet([1, 2, 3, 4, 5])", "addObjects: [1, 2, 3] + [3, 4, 5] == [1, 2, 3, 4, 5]")
        testObj3.delObjects(testObj1)
        self.assertEqual(repr(testObj3), "_P4OOSet([4, 5])", "delObjects: [1, 2, 3, 4, 5] - [1, 2, 3] == [4, 5]")

#    def test_Exceptions(self):
#        pass


if __name__ == '__main__':
    unittest.main()
