# -*- coding: utf8 -*-
import re

from django.test import TestCase
from django.test.utils import override_settings

from .base import UrlGetTestMixin


class RepresentativeListTest(UrlGetTestMixin, TestCase):
    fixtures = ['smaller_sample.json']
    url = '/representative/'

    # Cancel out constance with TEMPLATE_CONTEXT_PROCESSORS=[]
    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=[])
    def test_num_queries(self):
        with self.assertNumQueries(5):
            """
            - One query for the rep details and foreign key (profile)
            - One query for reverse relation on votes
            - One query for reverse relation on mandates
            - One query for reverse relation positions
            - One query for reverse relation tags on positions
            """
            response = self.client.get(self.url)

    def test_name_display(self):
        # When HAMLPY_ATTR_WRAPPER works, use double quotes in HTML attrs !
        assert "<h1 class='name'>Karima DELLI</h1>" in self.response.content
