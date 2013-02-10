#!/usr/bin/env python

import unittest
from nose.tools import eq_

from main import Main, find_emails


MULTILINE_INPUT = """blandit
jerome@880.com orci. ray@resumes.com Ut eu diam at pede suscipit
sodales. Aenean lectus elit, fermentum
"""


class EmailParseTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_runs(self):
        """Ensure that the program runs"""

        p = Main()
        p.run()

    def text_no_matches(self):
        text= """laoreet. Donec lacus nunc, viverra nec, blandit ve"""
        matches = find_emails(text)
        eq_(len(matches), 0)

    def test_single_line_email(self):
        text = "*steve@stevechallis.com asda s"
        matches = find_emails(text, multiline=False)
        eq_(len(matches), 1)

    def test_non_multiline_emails(self):
        matches = find_emails(MULTILINE_INPUT, multiline=False)
        eq_(len(matches), 2)
        eq_(matches, ['jerome@880.com', 'ray@resumes.com'])

    def test_multiline_emails(self):
        matches = find_emails(MULTILINE_INPUT, multiline=True)
        eq_(len(matches), 2)
        eq_(matches, ['blanditjerome@880.com', 'ray@resumes.com'])


if __name__ == '__main__':
    unittest.main()
