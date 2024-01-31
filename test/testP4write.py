#!/usr/bin/env python3

######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#  Copyright (c)2012 Cisco Systems, Inc.
#
#  testP4oopy.py
#
######################################################################

######################################################################
# Includes
#
import P4
from P4OO.Branch import P4OOBranch
from P4OO.Label import P4OOLabel
from P4OO.Client import P4OOClient
from P4OO.Change import P4OOChange
from P4OO._P4Python import _P4OOP4Python
import logging

######################################################################
# MAIN
#
p4PythonObj = P4.P4()
p4PythonObj.port = "localhost:1667"
p4PythonObj.connect()                   # Connect to the Perforce Server
info = p4PythonObj.run("info")[0]
print("serverAddress: ", info['serverAddress'])

logging.basicConfig(level=logging.DEBUG)

#p4b1Dict = {'Description': 'This is only a test', 'Branch': 'fooo'}
#print(p4PythonObj.run("branch"
#
#exit()

# Create a branch from id
#p4b1 = P4OOBranch(id="newfromID", p4PythonObj=p4PythonObj)
#p4b1.saveSpec()
#exit()

# Create a branch from specAttr
#p4b2 = P4OOBranch(p4PythonObj=p4PythonObj)
#p4b2._setSpecAttr("Branch", "newfromattr")
#p4b2.saveSpec()
#
#exit()

p4c1 = P4OOChange(p4PythonObj=p4PythonObj)
p4c1._setSpecAttr("Description", "testing 'new' change")
p4c1.saveSpec()
#print("new change#: ", p4c1._getAttr('modifiedSpec'))
print("new change#: ", p4c1)
exit()

# Create a new client with no id
p4cl1 = P4OOClient(p4PythonObj=p4PythonObj)
p4cl1.saveSpec()
exit()


#p4b1 = P4OOBranch(id="foooo", p4PythonObj=p4PythonObj)
p4b1 = P4OOBranch(id="foooo", p4PythonObj=p4PythonObj)
#print(p4b1._toJSON())
p4b1._setSpecAttr("Branch", "fooo")
p4b1._setSpecAttr("Description", "This is only a test")
print(p4b1.__dict__)
p4b1.saveSpec()
print(p4b1.__dict__)
p4b1._setSpecAttr("Description", "This is the second test")
print(p4b1.__dict__)
p4b1.saveSpec()
print(p4b1.__dict__)

exit()

#p4b2 = P4OOBranch( id="infraMain" )
p4b2 = P4OOBranch( id="infraMain", p4PythonObj=p4PythonObj )
print("p4b2: ", p4b2)
print("Description2: " + p4b2._getSpecAttr("Description"))

#p4cl1 = P4OOClient( id="Davids-MacBook-Air" )
#p4ch1 = P4OOChange( id=34 )
#p4ch2 = P4OOChange( id=68 )
#
#p4Changes = p4ch1.getChangesFromChangeNums(p4ch2, p4cl1)
#print('p4Changes: ', p4Changes)
#
##print([change._getSpecID() for change in p4Changes])
#print([id(change) for change in p4Changes])
#
#print()
#print('changes: ', p4Changes.listObjectIDs())
#print( p4Changes[-34] )
##print(p4Changes.listObjects())
#
#p4l1 = P4OOLabel( id="P4-OO-0.00_01" )
#print("p4l1 last change: ", id(p4l1.getLastChange()))
#
#p4l2 = P4OOLabel( id="P4-OO-0.00_02" )
#print("p4l2 last change: ", id(p4l2.getLastChange()))
#
#print("changes from p4l1 to p4l2: ", p4l1.getChangesFromLabels(p4l2, p4cl1))
#
#date = p4ch2._getSpecAttr('Date')
#print("p4ch2 Date: %s" % date)
#
#print("\n opened files: ", p4cl1.getOpenedFiles())
#
#print("label diffs: ", '\n'.join(p4l1.getDiffsFromLabels(p4l2, p4cl1)))
