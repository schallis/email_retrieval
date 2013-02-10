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

    def __init__(self, test=False):
        """Setup our program based upon the command line arguments"""

        self.test = test
        self.options = self.parse_args()
        self.matches = []

        if not self.options.quiet and not self.test:
            handler = logging.StreamHandler(sys.stdout)
            LOGGER.setLevel(logging.DEBUG)
            LOGGER.addHandler(handler)
            LOGGER.debug(_('Using verbose mode'))

    def parse_args(self):
        """Build a list of options based on user input and return them"""

        option_list = [
            make_option("-q", "--quiet", action="store_true", dest="quiet"),
            make_option("-s", "--stdin", action="store_true", dest="stdin"),
            make_option("-f", "--file", action="store", type="string", dest="path"),
            make_option("-u", "--url", action="store", type="string", dest="url"),
            make_option("-o", "--output", action="store", type="string", dest="output"),
        ]
        parser = OptionParser(option_list=option_list)
        options, __ = parser.parse_args()

        return options

    def write_to_file(self, outfile, matches):
        try:
            with open(outfile, 'w') as output:
                output.write('\n'.join(matches))
        except IOError:
            LOGGER.error(_('Invalid output file specified'))


    def output(self):
        """Display or write matches to file"""

        matches = self.get_matches()
        if not matches:
            print _('No matches found')
            sys.exit(1)
        print _("Found {0} matches".format(len(matches)))

        if self.options.output:
            outfile = self.options.output
            self.write_to_file(outfile, matches)
        else:
            print matches

    def get_matches(self):
        """Return the list of matched emails as a list"""

        return self.matches

    def read_from_stdin(self):
        """Read, parse and return any found emails from stdin"""

        matches = []
        with sys.stdin as infile:
            for line in infile:
                matches.extend(find_emails(line))
        return matches

    def read_from_url(self, url):
        """Read, parse and return any found emails from `url`"""

        # TODO: cleanup url (add slashes, protocol)
        try:
            root = parse(url).getroot()
        except IOError:
            LOGGER.error(_('Unable to parse input URL'))
            sys.exit(1)
        if root is not None:
            text = root.text_content()
        else:
            LOGGER.error(_('Bad URL, cannot find document root'))
            sys.exit(1)

        return find_emails(text)

    def read_from_file(self, infile):
        """Read, parse and return any found emails from `infile`"""

        matches = []
        try:
            with open(infile) as f:
                for line in f:
                    self.matches.extend(find_emails(line))
        except IOError:
            LOGGER.error(_('Unable to read file'))
            sys.exit(1)


        return matches

    def run(self):
        """Get the party started"""

        if self.options.path:
            infile = self.options.path
            LOGGER.debug(_('Reading from file {0}...').format(infile))
            self.matches.extend(self.read_from_file(infile))
        elif self.options.url:
            url = self.options.url
            LOGGER.debug(_('Reading from url {0}...').format(url))
            self.matches.extend(self.read_from_url(url))
        elif self.options.stdin:
            LOGGER.debug(_('Reading from stdin...'))
            self.matches.extend(self.read_from_stdin())
        elif not self.test:
            LOGGER.error(_('No input method specified'))
            sys.exit(1)


if __name__ == '__main__':
    p = Main()
    p.run()
    p.output()
