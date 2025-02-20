# Welcome

## Introduction

Welcome to P4OO.py!  P4OO.py provides a layer of first class objects on
top of P4Python.  The concept is to bring order to managing Perforce in
a programmatic fashion, building on top of the command-driven API.

The standard C, Perl, and Python APIs for Perforce are essentially
equivalent to the commandline client, with some rudimentary capabilities
for returning native structures instead of strings to be parsed.  The
value added is significant, with reusable connections and reduced parsing.

P4OO.py takes it to the next level.  In some cases using the stock APIs
the output must still be parsed to understand what happened (such as with
'p4 submit' to determine the new change number).  In all cases, the
output returned from the API must still be "understood", in that it's
not always self-descriptive.  It's usually an anonymous list of anonymous
dicts, and so the caller must have hardcoded intelligence to wrap and
decode every API call.

P4OO tries to take care of all of the wrapping and decoding for you.
Methods are provided on first class objects to construct the appropriate
Perforce commands, and the output is neatly parsed and converted into
other first class P4OO.py objects where applicable.

## For More Information

See the current version of the documentation available on
[GitHub Pages](https://daversomethingsomethingorg.github.io/P4OO.py)

## Installation

Installation is currently manual using 'pip install .'  A PyPI general
release is coming soon.

## Dependencies

This module requires these other modules and libraries:

- **P4Python**

    For direct Perforce connection, P4Python is required, provided by
    Perforce under their own license and Copyright.
    <https://www.perforce.com/manuals/p4python/Content/P4Python/Home-p4python.html>

- **PyYAML**

    P4OO.py uses a YAML configuration file, PyYAML is used to read it.

## Related

- **P4::OO**
    P4OO.py is derived from the Perl P4::OO module that can be found on CPAN:
    <http://search.cpan.org/~armstd/P4-OO-0.00_02/lib/P4/OO.pm>

## Copyright and License

Copyright (C) 2011-2015,2024 by David L. Armstrong
Some Parts Copyright (C) 2011-2015,2024 by David L. Armstrong and Cisco Systems, Inc.

This package is distributed under the terms of the Artistic License 2.0.
For more details, see the full text of the license in the file LICENSE.

## Support and Warranty

This program is distributed in the hope that it will be useful, but
it is provided "as is" and without any expressed or implied warranties.
For details, see the full text of the license in the file LICENSE.
