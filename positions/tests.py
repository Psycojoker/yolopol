import datetime
import copy

from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser

from legislature.models import MemopolRepresentative
from positions.models import Position


class PositionCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tags = [u'foo', u'bar']

        self.mep = MemopolRepresentative.objects.create(
                full_name='position create test', slug='position-create-test')

        self.fixture = {
            'tags': ','.join(self.tags),
            'datetime': '2015-12-11',
            'text': 'bla',
            'link': 'http://example.com/bar',
            'representative': self.mep.pk,
        }

    def test_create_position(self):
        response = self.client.post('/positions/create', self.fixture)
        expected = 'http://testserver/legislature/position-create-test'
        assert response['Location'] == expected

        result = Position.objects.get(text='bla')
        assert list(result.tags.values_list('name', flat=True)) == self.tags
        assert result.datetime == datetime.date(2015, 12, 11)
        assert result.link == self.fixture['link']
        assert result.representative.representative_ptr_id == self.mep.pk

    def test_create_position_without_field(self):
        for key in self.fixture.keys():
            fixture = copy.copy(self.fixture)
            fixture.pop(key)

            response = self.client.post('/positions/create', fixture)
            assert response.context['form'].is_valid() is False
