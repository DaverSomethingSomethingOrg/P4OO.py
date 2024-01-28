######################################################################
#  Copyright (c)2013, Cisco Systems, Inc.
#
#  _P4GoldenEgg.py
#
######################################################################

#NAME / DESCRIPTION
'''
_P4GoldenEgg - save and restore pre-populated Perforce databases
from tarballs, intended for use in testing.
'''

######################################################################
# Includes
#
import tarfile

######################################################################
# P4Python Class Initialization
#
class eggTarball(object):
    ######################################################################
    # Methods
    #
    def __init__(self, tarball):
        self.tarball = tarball

    ######################################################################
    # unpack( directory )
    #  Unpack tarball into the specified directory
    #
    # NOTES:
    #
    def unpack(self, directory):
        tarfile.open(name=self.tarball).extractall(path=directory)
        eggDir = eggDirectory(directory=directory)
        return eggDir


class eggDirectory(object):
    ######################################################################
    # Methods
    #
    def __init__(self, directory):
        self.directory = directory

    ######################################################################
    # getP4Port( p4d )
    #  Create a tarball from the current object and store it in the new
    #  location specified
    #
    # NOTES:
    #   P4PORT="rsh:p4d -r /var/p4root -i"
    #
    def getP4Port(self, p4d):
        return("rsh:%s -r %s -i" % (p4d, self.directory))

    ######################################################################
    # create( newTarball )
    #  Create a tarball from the current object and store it in the new
    #  location specified
    #
    # NOTES:
    #
    def createTarball(self, tarball):
        tarObj = tarfile.open(name=tarball, mode='w:gz')
        tarObj.add(self.directory, arcname=".")
        tarObj.close()

        eggBall = eggTarball(tarball=tarball)
        return eggBall

    ######################################################################
    # destroy()
    #  Remove the unpacked Egg directory
    #
    # NOTES:
    #
    def destroy(self):
#        eggBall = eggTarball(tarball=tarball)
#        return eggBall
        pass
