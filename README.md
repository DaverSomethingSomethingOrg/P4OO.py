# P4OO.py

## Introduction

Welcome to P4OO.py!  P4OO.py (based on the Perl P4::OO module) provides a layer of first class objects on top of P4Python.  The concept is to bring order to managing Perforce in a programmatic fashion, rather than simply treating Perforce as a set of commands to be run in sequence.

The standard C, Perl, and Python APIs are essentially equivalent to the commandline client, with some rudimentary capabilities for returning native structures instead of strings to be parsed.  The value added is significant, with reusable connections and reduced parsing, but P4OO.py takes it to the next level.  In some cases using the stock APIs the output must still be parsed to understand what happened (such as with 'p4 submit' to determine the new change number).  In all cases, the output returned from the API must still be "understood", in that it's not always self-descriptive.  It's usually an anonymous list of anonymous dicts, and so the caller must have hardcoded intelligence to wrap and decode every API call.

P4OO tries to take care of all of the wrapping and decoding for you.  Methods are provided on first class objects to construct the appropriate Perforce commands, and the output is neatly parsed and converted into other first class objects where applicable.

# INSTALLATION

Installation is currently manual.  The code is pure Python, so it'll "just work" from the directory it is downloaded into.

# DEPENDENCIES

This module requires these other modules and libraries:

*   **P4Python**  
    For direct Perforce connection, P4Python is required, provided by Perforce under their own license and Copyright.  
    http://www.perforce.com/perforce/doc.current/manuals/p4script/03_python.html
*   **PyYAML**  
    P4OO.py uses a YAML configuration file, PyYAML is used to read it.

# RELATED
*   **P4::OO**  
    P4OO.py is derived from the Perl P4::OO module that can be found on CPAN:  
    http://search.cpan.org/~armstd/P4-OO-0.00_02/lib/P4/OO.pm


# COPYRIGHT AND LICENCE

Copyright (C) 2011-2015,2024 by David L. Armstrong, Cisco Systems, Inc.

This package is distributed under the terms of the Artistic License 2.0.
For more details, see the full text of the license in the file LICENSE.

# SUPPORT AND WARRANTY

This program is distributed in the hope that it will be useful, but
it is provided "as is" and without any expressed or implied warranties.
For details, see the full text of the license in the file LICENSE.

