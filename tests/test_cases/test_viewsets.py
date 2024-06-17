from unittest import TestCase

from django.core.checks.urls import check_url_config


class TestViewSet(TestCase):
    def test_url_config(self):
        check_url_config(None)
