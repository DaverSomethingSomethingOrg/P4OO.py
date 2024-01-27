#!/usr/bin/env python3.2

######################################################################
#  Copyright (c)2013, Cisco Systems, Inc.
#
#  test/P4OO/Client.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
'''
unittest test suite for P4OO.Client
'''

######################################################################
# Includes
#
import os  # used for managing environment variables
import sys # used her for include path mgmt
sys.path.append('/home/dave/p4/dave_pan/projects/p4oopy/main/lib')

import P4OO.Client
import logging



######################################################################
# MAIN
#
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    testClient = P4OO.Client.P4OOClient(id="dave_pan_2")
    testClient.sync("//dave_pan_2/projects/p4oopy/main/lib/P4OO/Client.py", force=1)


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
