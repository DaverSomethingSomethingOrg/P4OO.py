#!/usr/bin/env python3.2

######################################################################
#  Copyright (c)2011-2012, David L. Armstrong.
#  Copyright (c)2012-2013, Cisco Systems, Inc.
#
#  testP4oopy.py
#
#  See COPYRIGHT AND LICENSE section in pod text below for usage
#   and distribution rights.
#
######################################################################

######################################################################
# Include Paths
#
import sys
sys.path.append('../lib')


######################################################################
# Includes
#
from P4OO.Branch import P4OOBranch
from P4OO.Label import P4OOLabel
from P4OO.Client import P4OOClient
from P4OO.Change import P4OOChange
from P4OO._P4Python import _P4OOP4Python
import pprint
import logging

######################################################################
# MAIN
#

logging.basicConfig(level=logging.DEBUG)


p4b2 = P4OOBranch( id="infraMain" )
print("p4b2: ", p4b2)
print("Description2: " + p4b2._getSpecAttr("Description"))

p4cl1 = P4OOClient( id="Davids-MacBook-Air" )
p4ch1 = P4OOChange( id=34 )
p4ch2 = P4OOChange( id=68 )

p4Changes = p4ch1.getChangesFromChangeNums(p4ch2, p4cl1)
print('p4Changes: ', p4Changes)

#print([change._getSpecID() for change in p4Changes])
print([id(change) for change in p4Changes])

print()
print('changes: ', p4Changes.listObjectIDs())
print( p4Changes[-34] )
#print(p4Changes.listObjects())

p4l1 = P4OOLabel( id="P4-OO-0.00_01" )
print("p4l1 last change: ", id(p4l1.getLastChange()))

p4l2 = P4OOLabel( id="P4-OO-0.00_02" )
print("p4l2 last change: ", id(p4l2.getLastChange()))

print("changes from p4l1 to p4l2: ", p4l1.getChangesFromLabels(p4l2, p4cl1))

date = p4ch2._getSpecAttr('Date')
print("p4ch2 Date: %s" % date)

print("\n opened files: ", p4cl1.getOpenedFiles())

print("label diffs: ", '\n'.join(p4l1.getDiffsFromLabels(p4l2, p4cl1)))


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
# Copyright (c)2012-2013, Cisco Systems, Inc.
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
