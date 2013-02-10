#!/usr/bin/env python

# Copyright 2013 Steve Challis.
#
# This is Free Software, licenced under the GNU General Public
# License ("GPL").  Version 3 of the GPL shall apply unless a
# later version has been published by the Free Software
# Software Foundation ("FSF") at the time you receive this
# software, in which case that later version shall apply instead.
# At your your option, you may apply any version of the GPL
# published by the FSF later than that prescribed above.
#
# This software is supplied "as is" and "with all faults".
# There is ABSOLUTELY NO WARRANTY.  Please refer to the relevant
# section of the licence for more details.
#
# If you do not have a copy of the licence, please refer to
# <http://www.gnu.org/licenses/>

# steve@stevechallis.com
# Feb 2013

__author__ = 'Steve Challis'

import re
import sys
import logging
from optparse import OptionParser, make_option


LOGGER = logging.getLogger(__name__)
EMAIL_RE = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}', re.IGNORECASE)


def find_emails(text, multiline=False):
    """Return a list of all non-overlapping emails matched in text

    Will match emails that span multiple lines if the `multiline` param is True
    """
    if multiline:
        text = text.replace('\r\n', '').replace('\n', '')
    return re.findall(EMAIL_RE, text)


class Main(object):

    def __init__(self):
        """Setup our program based upon the command line arguments"""

        option_list = [
            make_option("-v", "--verbose", action="store_true", dest="verbose"),
            make_option("-f", "--file", action="store", type="string", dest="file"),
            make_option("-u", "--url", action="store", type="string", dest="url"),
            make_option("-o", "--output", action="store", type="string", dest="output"),
        ]
        parser = OptionParser(option_list=option_list)
        self.options, args = parser.parse_args()
        self.matches = []

        if self.options.verbose:
            handler = logging.StreamHandler(sys.stdout)
            LOGGER.setLevel(logging.DEBUG)
            LOGGER.addHandler(handler)
            LOGGER.debug('Using verbose mode')

    def output(self):
        """Display or write matches to file"""
        if self.options.output:
            with open(self.output, 'w') as out_file:
                output.writelines(self.matches)
        else:
            print self.matches

    def run(self):
        """Get the party started"""

        if self.options.file:
            file = self.options.file
            LOGGER.debug('Reading from file {0}'.format(file))
            with open(file) as f:
                for line in f:
                    self.matches.extend(find_emails(line))

        if self.matches:
            self.output()

if __name__ == '__main__':
    p = Main()
    p.run()
