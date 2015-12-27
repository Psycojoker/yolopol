import re

from django.test import Client


class UrlGetTestMixin(object)
    url = None

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
