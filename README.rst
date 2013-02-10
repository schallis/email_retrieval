============
Email Parser
============

:Info: A utility app for reading text sources and finding email addresses
:Authors: Steve Challis (http://schallis.com)
:Requires: Python 2.7, (see others in requirements.pip)
:License: Distributed under the GPL V3

Installation and Usage
======================

The application can be run with (from stdin)::

    echo "My email is steve@stevechallis.com" | ./main.py --stdin

A list of optional arguments can be found by running::

    ./main.py -h

The test suite can be run with::

    ./tests
