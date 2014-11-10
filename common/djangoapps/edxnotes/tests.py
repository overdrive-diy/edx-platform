"""
Unit tests for the EdxNotes app.
"""

import collections
from mock import patch
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from . import helpers


class HelpersTest(TestCase):
    def setUp(self):
        '''
        Setup a dummy course-like object with a tabs field that can be
        accessed via attribute lookup.
        '''
        self.course = collections.namedtuple('DummyCourse', ['tabs'])
        self.course.tabs = []

    def test_edxnotes_not_enabled(self):
        '''
        Tests that edxnotes are disabled when the course tab configuration does NOT
        contain a tab with type "edxnotes."
        '''
        self.assertFalse(helpers.edxnotes_enabled_for_course(self.course))

    def test_edxnotes_enabled(self):
        '''
        Tests that edxnotes are enabled when the course tab configuration contains
        a tab with type "edxnotes."
        '''
        self.course.tabs = [{'type': 'foo'},
                            {'name': 'Notes', 'type': 'edxnotes'},
                            {'type': 'bar'}]

        self.assertTrue(helpers.edxnotes_enabled_for_course(self.course))

    def test_storage_url(self):
        '''
        Tests that storage_url method returns correct values.
        '''
        with patch.dict('django.conf.settings.EDXNOTES_INTERFACE', {'url': 'http://example.com/'}):
            self.assertEqual('http://example.com/api/v1', helpers.get_storage_url())

        with patch.dict('django.conf.settings.EDXNOTES_INTERFACE', {'url': 'http://example.com'}):
            self.assertEqual('http://example.com/api/v1', helpers.get_storage_url())

        with patch.dict('django.conf.settings.EDXNOTES_INTERFACE', {'url': None}):
            self.assertRaises(ImproperlyConfigured, helpers.get_storage_url)
