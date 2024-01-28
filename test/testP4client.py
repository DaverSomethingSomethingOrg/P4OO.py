#!/usr/bin/env python3

######################################################################
#  Copyright (c)2013, Cisco Systems, Inc.
#
#  test/P4OO/Client.py
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

import P4OO.Client
import logging



######################################################################
# MAIN
#
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    testClient = P4OO.Client.P4OOClient(id="dave_pan_2")
    testClient.sync("//dave_pan_2/projects/p4oopy/main/lib/P4OO/Client.py", force=1)
