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
from collections import defaultdict
from gettext import gettext as _
from optparse import OptionParser, make_option

from lxml.html import parse


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

        self.options = self.parse_args()
        self.matches = []

        if not self.options.quiet:
            handler = logging.StreamHandler(sys.stdout)
            LOGGER.setLevel(logging.DEBUG)
            LOGGER.addHandler(handler)
            LOGGER.debug(_('Using verbose mode'))

    def parse_args(self):
        option_list = [
            make_option("-q", "--quiet", action="store_true", dest="quiet"),
            make_option("-s", "--stdin", action="store_true", dest="stdin"),
            make_option("-f", "--file", action="store", type="string", dest="file"),
            make_option("-u", "--url", action="store", type="string", dest="url"),
            make_option("-o", "--output", action="store", type="string", dest="output"),
        ]
        parser = OptionParser(option_list=option_list)
        options, __ = parser.parse_args()
        return options

    def output(self):
        """Display or write matches to file"""
        print _("Found matches")
        if self.options.output:
            with open(self.output, 'w') as out_file:
                output.writelines(self.matches)
        else:
            print self.matches

    def run(self):
        """Get the party started"""

        if self.options.file:
            infile = self.options.file
            LOGGER.debug(_('Reading from file {0}...').format(infile))
            with open(infile) as f:
                for line in f:
                    self.matches.extend(find_emails(line))
        if self.options.url:
            # TODO: cleanup url (add slashes, protocol)
            url = self.options.url
            LOGGER.debug(_('Reading from url {0}...').format(url))
            root = parse(url).getroot()
            if root:
                text = root.text_content()
            else:
                raise Exception(_('Bad URL, cannot find document root'))
            self.matches.extend(find_emails(text))
        elif self.options.stdin:
            LOGGER.debug(_('Reading from stdin...'))
            with sys.stdin as infile:
                for line in infile:
                    self.matches.extend(find_emails(line))
        else:
            raise Exception(_('No input method specified'))


if __name__ == '__main__':
    p = Main()
    p.parse_args()
    p.run()
    p.output()
