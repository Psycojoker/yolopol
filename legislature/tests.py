# -*- coding: utf8 -*-
import re

from django.test import TestCase, Client
from django.test.utils import override_settings

class RedisplayativeDetailTest(TestCase):
    fixtures = ['one_representative.json']

    def setUp(self):
        self.client = Client()

        if not hasattr(self, 'response'):
            # Do it once and for all, note that this also caches content types
            # so the contenttype query used by taggit won't be counted in
            # test_num_queries.
            self.response = self.client.get('/legislature/karima-delli')

    # Cancel out constance with TEMPLATE_CONTEXT_PROCESSORS=[]
    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=[])
    def test_num_queries(self):
        with self.assertNumQueries(5):
            response = self.client.get('/legislature/karima-delli')

    def test_name_display(self):
        # When HAMLPY_ATTR_WRAPPER works, use double quotes in HTML attrs !
        assert "<h1 class='name'>Karima DELLI</h1>" in self.response.content

    def test_score_display(self):
        assert '<span class="label label-success">233</span>' in self.response.content

    def test_country_display(self):
        assert re.findall('<span class="flag-icon flag-icon-fr"></span>\s+France', self.response.content)  # noqa

    def test_current_mandate_display(self):
        assert re.findall("<a href='/legislature/group/Greens/EFA'>\s+Member of\s+Group of the Greens/European Free Alliance\s+</a>", self.response.content)  # noqa

    def test_biography_display(self):
        assert re.findall('Born in Roubaix the\s+04/03/1979\s+\(F\)', self.response.content)  # noqa

    def test_mandates_display(self):
        # Pieces of data taken from various rows of the mandate table
        data = [
            '/legislature/committee/FEMM',
            'Committee on Women&#39;s Rights and Gender Equality (FEMM)',
            '01/07/2014',
            '/legislature/group/Greens/EFA',
            'Group of the Greens/European Free Alliance (Greens/EFA)',
            '/legislature/country/FR',
            'Europe Écologie',
        ]

        for d in data:
            assert d in self.response.content, '%s not found' % d

    def test_votes_display(self):
        raise NotImplemented()

    def test_proposal_display(self):
        raise NotImplemented()

# group-index(kind)
# redisplayative-detail(name)
# redisplayative-detail(pk)
# redisplayative-index(group_kind)(group)
# redisplayative-index(active)
