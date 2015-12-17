from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser

from legislature.models import MemopolRepresentative
from positions.models import Position

# position-create
# position-detail(pk)

class PositionCreateTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_position(self):
        client = Client()
        mep = MemopolRepresentative.objects.create(
                full_name='PositionCreateTest test_create_position',
                slug='PositionCreateTest-test_create_position')

        import ipdb; ipdb.set_trace()
        client.post('/positions/create', {
            'tags': 'foo,bar',
            'datetime': '2015-12-11',
            'text': 'bla',
            'link': 'http://example.com/bar',
            'representative': mep.pk
        })
