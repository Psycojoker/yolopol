import datetime
import copy

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from representatives.models import Representative
from representatives_positions.models import Position


class PositionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tags = [u'foo', u'bar']
        self.create_url = reverse('representatives_positions:position-create')

        self.mep = Representative.objects.create(
            full_name='%sfull' % self.id(), slug='slug')

        self.fixture = {
            'tags': ','.join(self.tags),
            'datetime': '2015-12-11',
            'text': '%stext' % self.id(),
            'link': 'http://example.com/%slink' % self.id(),
            'representative': self.mep.pk,
        }

    def test_create_position(self):
        response = self.client.post(self.create_url, self.fixture)
        assert response.status_code == 302
        expected = 'http://testserver/representative/slug/'
        assert response['Location'] == expected

        result = Position.objects.get(text='%stext' % self.id())
        assert list(result.tags.values_list('name', flat=True)) == self.tags
        assert result.datetime == datetime.date(2015, 12, 11)
        assert result.link == self.fixture['link']
        assert result.representative.pk == self.mep.pk
        assert result.published is False

    def test_position_publishing(self):
        response = self.client.post(self.create_url, self.fixture)
        assert response.status_code == 302
        position = Position.objects.get(text='%stext' % self.id())

        get_response = self.client.get(position.get_absolute_url())
        assert get_response.status_code == 404

        position.published = True
        position.save()

        get_response = self.client.get(position.get_absolute_url())
        assert get_response.status_code == 200

    def test_create_position_without_field(self):
        for key in self.fixture.keys():
            fixture = copy.copy(self.fixture)
            fixture.pop(key)

            response = self.client.post(self.create_url, fixture)
            assert response.context['form'].is_valid() is False, \
                'Could submit form without %s' % key

    def test_position_detail(self):
        fixture = copy.copy(self.fixture)
        fixture['representative'] = self.mep
        fixture.pop('tags')

        position = Position.objects.create(published=True, **fixture)
        position.tags.add('%stag' % self.id())

        with self.assertNumQueries(4):
            response = self.client.get(position.get_absolute_url())

        assert 'Dec. 11, 2015' in response.content
        assert '%stag' % self.id() in response.content
        assert fixture['link'] in response.content
        assert fixture['text'] in response.content
        assert self.mep.full_name in response.content
