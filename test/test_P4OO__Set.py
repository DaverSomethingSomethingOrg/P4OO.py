#!/usr/bin/env python3

######################################################################
#  Copyright (c)2012,2024 David L. Armstrong
#
#  test/test_P4OO__Set.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce _Set unittest Class

'''

######################################################################
# Includes
#
import P4OO._Base
import P4OO._Set
import P4OO._OrderedSet
#import pytest

def test_setConstruction():
    testObj1 = P4OO._Set._P4OOSet(iterable=[1, 2, 3])
    assert isinstance(testObj1, P4OO._Set._P4OOSet)
    assert isinstance(testObj1, P4OO._OrderedSet.OrderedSet)
    assert isinstance(testObj1, P4OO._Base._P4OOBase)

    # "repr() for set [1, 2, 3] returns '_P4OOSet([1, 2, 3])'")
    assert repr(testObj1) == "_P4OOSet([1, 2, 3])"

    # "copy constructor gives same repr()")
    testObj2 = P4OO._Set._P4OOSet(iterable=testObj1)
    assert repr(testObj2) == "_P4OOSet([1, 2, 3])"

    testObj3 = P4OO._Set._P4OOSet(iterable=['a', 'b', 'c'])
    # "repr() for set ['a', 'b', 'c'] returns '_P4OOSet(['a', 'b', 'c'])'")
    assert repr(testObj3) == "_P4OOSet(['a', 'b', 'c'])"


def test_setSetFunctionality():
    testObj1 = P4OO._Set._P4OOSet(iterable=[1, 2, 3])
    testObj2 = P4OO._Set._P4OOSet(iterable=[3, 4, 5])

    # "len([1, 2, 3]) is 3"
    assert len(testObj1) == 3

    testObj3 = testObj1 & testObj2
    print(testObj1, testObj2, testObj3)
    assert isinstance(testObj3, P4OO._Set._P4OOSet)

    # "intersection: [1, 2, 3] & [3, 4, 5] == [3]"
    assert repr(testObj3) == "_P4OOSet([3])"

    testObj4 = testObj1 | testObj2
    # "union: [1, 2, 3] | [3, 4, 5] == [1, 2, 3, 4, 5]"
    assert repr(testObj4) == "_P4OOSet([1, 2, 3, 4, 5])"

    # "len([1, 2, 3, 4, 5]) is 5"
    assert len(testObj4) == 5

    testObj4.add(3)

    # "add(3) to [1, 2, 3, 4, 5] stays the same"
    assert repr(testObj4) == "_P4OOSet([1, 2, 3, 4, 5])"

    # "len([1, 2, 3, 4, 5]) is 5"
    assert len(testObj4) == 5

    testObj4.add(6)

    # "add(6) to [1, 2, 3, 4, 5] makes [1, 2, 3, 4, 5, 6]"
    assert repr(testObj4) == "_P4OOSet([1, 2, 3, 4, 5, 6])"

    # "len([1, 2, 3, 4, 5, 6]) is 6"
    assert len(testObj4) == 6

    testObj4.discard(0)

    # "discard(0) from [1, 2, 3, 4, 5, 6] stays the same"
    assert repr(testObj4) == "_P4OOSet([1, 2, 3, 4, 5, 6])"

    # "len([1, 2, 3, 4, 5, 6]) is 6"
    assert len(testObj4) == 6

    testObj4.discard(6)

    # "discard(6) from [1, 2, 3, 4, 5, 6] makes [1, 2, 3, 4, 5]"
    assert repr(testObj4) == "_P4OOSet([1, 2, 3, 4, 5])"

    # "len([1, 2, 3, 4, 5]) is 5"
    assert len(testObj4) == 5


def test_setSetAddDel():
    testObj1 = P4OO._Set._P4OOSet(iterable=[1, 2, 3])
    testObj2 = P4OO._Set._P4OOSet(iterable=[3, 4, 5])
    testObj3 = P4OO._Set._P4OOSet(iterable=testObj1)  # copy the set, don't just assign
    testObj3.addObjects(testObj2)

    # "addObjects: [1, 2, 3] + [3, 4, 5] == [1, 2, 3, 4, 5]"
    assert repr(testObj3) == "_P4OOSet([1, 2, 3, 4, 5])"

    testObj3.delObjects(testObj1)

    # "delObjects: [1, 2, 3, 4, 5] - [1, 2, 3] == [4, 5]"
    assert repr(testObj3) == "_P4OOSet([4, 5])"

#    def test_Exceptions(self):
#        pass
