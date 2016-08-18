from django import test
from responsediff.test import ResponseDiffTestMixin


class BaseTest(ResponseDiffTestMixin, test.TestCase):
    fixtures = ['smaller_sample.json']

    """
    Common queries
    - One for chambers
    - One for countries
    - One for parties
    - One for committees
    - One for delegations
    """
    left_pane_queries = 5

    def selector_test(self, selector, url=None):
        self.assertResponseDiffEmpty(self.client.get(url or self.url),
                                     selector)
