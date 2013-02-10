#!/usr/bin/env python

from mock import Mock, patch, call
import unittest
from nose.tools import eq_

from main import Main, find_emails


MULTILINE_INPUT = """blandit
jerome@880.com orci. ray@resumes.com Ut eu diam at pede suscipit
sodales. Aenean lectus elit, fermentum
"""


class EmailParseTest(unittest.TestCase):

    def setUp(self):
        self.test_options = Mock(
            quiet=True,
            stdin=None,
            path=None,
            url=None,
            output=None)

    def test_runs(self):
        """Ensure that the program runs"""

        program = Main(test=True)
        program.run()

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

    @patch('main.Main.read_from_stdin')
    @patch('main.Main.parse_args')
    def test_stdin(self, parse_args, stdin_patch):
        emails = ['test@test.com']
        stdin_patch.return_value = emails
        options = self.test_options
        options.stdin = True
        parse_args.return_value = options

        program = Main(test=True)
        program.run()

        eq_(program.get_matches(), emails)
        eq_(stdin_patch.call_count, 1)

    @patch('main.Main.read_from_url')
    @patch('main.Main.parse_args')
    def test_url(self, parse_args, url_patch):
        emails = ['test@test.com']
        url_patch.return_value = emails
        options = self.test_options
        options.url = 'test_url'
        parse_args.return_value = options

        program = Main(test=True)
        program.run()

        eq_(program.get_matches(), emails)
        eq_(url_patch.call_count, 1)
        eq_(url_patch.call_args, call('test_url'))

if __name__ == '__main__':
    unittest.main()
