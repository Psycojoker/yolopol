# -*- coding: utf8 -*-
import re

from django.test import TestCase, Client
from django.test.utils import override_settings

class RepresentativeDetailTest(TestCase):
    fixtures = ['one_representative.json']
    url = '/representative/karima-delli/'

    def setUp(self):
        self.client = Client()

        if not hasattr(type(self), 'response'):
            # Do it once and for all, note that this also caches content types
            # so the contenttype query used by taggit won't be counted in
            # test_num_queries.
            self.__class__.response = self.client.get(self.url)
        self.response = self.__class__.response

    def assertHtmlInResult(self, expected):
        compare = re.sub('[\s"\']', '', expected)
        result = re.sub('[\s"\']', '', self.response.content)
        assert compare in result

    def assertExpectedHtmlInResult(self):
        """
        For test_votes_display, it is:
        /positions/tests/test_representatives_detail_test_votes_display_expected.html
        """
        expected = __file__.replace('.py',
            '_%s_expected.html' % self._testMethodName)

        with open(expected, 'r') as f:
            self.assertHtmlInResult(f.read())

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
