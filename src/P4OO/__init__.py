######################################################################
#  Copyright (c)2011,2024 David L. Armstrong.
#
#  P4OO.__init__.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Object-Oriented Abstraction

P4OO provides a domain object modeled representation of Perforce.
It is designed to be easy to use, and to provide a natural OO
interface to Perforce.


Here's an example of retrieving the latest change on a particular
label:
    p4labelObj = P4OOLabel( id="P4-OO-0.00_01" )
    p4ChangeObj = p4l1.getLastChange()
    p4LastChangeId = p4ChangeObj.id
    
In this example, you'll see some patterns that are used throughout
the P4OO framework.  Methods will generally return other P4OO
objects, when the answers involve other Perforce entities.   These
returned objects will reuse the same P4Python handle for subsequent
queries.

The "id" attribute is used consistently throughout P4OO to identify
unique P4OO Spec objects, and is set to the name of the spec used
within Perforce.

When constructing a P4OO Spec object, only "id" is required.  Once
the object is constructed, you can use the object to query Perforce
for the other object attributes, such as the creator/owner of a label:

    p4labelObj = P4OOLabel( id="P4-OO-0.00_01" )
    p4LabelOwner = p4LabelObj._getSpecAttr("Owner")


'''
