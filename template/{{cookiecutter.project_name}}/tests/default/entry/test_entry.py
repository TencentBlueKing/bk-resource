# -*- coding: utf-8 -*-

from tests.base import TestCase
from django.test import override_settings

from tests.constants import TEST_MIDDLEWARE
from tests.default.entry.constants import ENTRY_DATA


class EntryTest(TestCase):
    """
    modules.default.entry
    """

    def test_entry(self):
        """
        test as resource
        """

        data = self.resource.entry.home()
        self.assertEqual(data, ENTRY_DATA)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_entry_url(self):
        """
        test as api url
        """

        data = self.client.get("/default/").data
        self.assertEqual(data, ENTRY_DATA)
