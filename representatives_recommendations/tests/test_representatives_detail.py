# -*- coding: utf8 -*-
import re

from django.test import TestCase
from django.test.utils import override_settings

from .base import UrlGetTestMixin


class RepresentativeDetailTest(UrlGetTestMixin, TestCase):
    fixtures = ['one_representative.json']
    url = '/representative/karima-delli/'

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

    def test_score_display(self):
        assert '<span class="label label-success">15</span>' in self.response.content

    def test_country_display(self):
        assert re.findall('<span class="flag-icon flag-icon-fr"></span>\s+France', self.response.content)  # noqa

    def test_current_mandate_display(self):
        expected = '''
        <a href="/representative/group/Greens/EFA/">
          Member of
          Group of the Greens/European Free Alliance
        </a>
        '''
        self.assertHtmlInResult(expected)

    def test_biography_display(self):
        assert re.findall('Born in Roubaix the\s+04/03/1979\s+\(F\)', self.response.content)  # noqa

    def test_votes_display(self):
        self.assertExpectedHtmlInResult()

    def test_mandates_display(self):
        self.assertExpectedHtmlInResult()

    def test_positions_display(self):
        self.assertExpectedHtmlInResult()
